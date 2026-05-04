import datetime
import os
from pathlib import Path

from celery import shared_task
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from reportlab.lib.colors import HexColor, black
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from contestadmin.models import Contest
from contestsuite.settings import MEDIA_ROOT
from register.models import Team as ContestTeam


CERTIFICATE_DIRNAME = 'certificates'

GARNET    = HexColor('#782F40')
PARCHMENT = HexColor('#F5EDD6')

_ASSETS_DIR = os.path.join(MEDIA_ROOT, 'certificate_assets')
_FONTS_DIR  = os.path.join(_ASSETS_DIR, 'fonts')
_FSU_LOGO   = os.path.join(_ASSETS_DIR, 'fsu.png')
_ACM_LOGO   = os.path.join(_ASSETS_DIR, 'acm.png')

_fonts_registered = False


def _register_fonts():
    global _fonts_registered
    if _fonts_registered:
        return
    pdfmetrics.registerFont(TTFont('MonteCarlo',            os.path.join(_FONTS_DIR, 'MonteCarlo-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('LibreBaskerville',      os.path.join(_FONTS_DIR, 'LibreBaskerville-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('LibreBaskerville-Bold', os.path.join(_FONTS_DIR, 'LibreBaskerville-Bold.ttf')))
    _fonts_registered = True


def _ordinal(n):
    suffix = 'th' if 11 <= (n % 100) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


def _get_placement(team):
    """Return 1-based rank of team within its division ordered by contest results."""
    ranked = ContestTeam.objects.filter(division=team.division).order_by(
        '-questions_answered', 'score', 'last_submission'
    )
    for rank, t in enumerate(ranked, 1):
        if t.pk == team.pk:
            return rank
    return None


def certificate_relative_path_for_user(user):
    """Return the relative media path for a user's certificate PDF."""
    team_name = user.profile.team.name if user.profile.has_team() else 'individual'
    filename = (
        f"participation_certificate_{user.pk}_"
        f"{slugify(user.get_full_name() or user.username)}_"
        f"{slugify(team_name)}.pdf"
    )
    return f"{CERTIFICATE_DIRNAME}/{filename}"


@shared_task
def generate_participation_certificate(user_id):
    """Create or overwrite a participation certificate PDF for a user."""
    _register_fonts()

    user = User.objects.select_related('profile', 'profile__team').get(pk=user_id)

    if not user.profile.has_team():
        raise ValueError('Participation certificates require the user to be on a team.')

    team = user.profile.team
    relative_path = certificate_relative_path_for_user(user)
    output_path = Path(MEDIA_ROOT) / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    contest = Contest.objects.first()
    granted_date = contest.contest_date if contest else datetime.date.today()
    granted = granted_date.strftime('%B %d, %Y')
    semester_name = 'Spring' if granted_date.month <= 7 else 'Fall'
    semester = f'{semester_name} {granted_date.year}'

    pw, ph = landscape(letter)   # 792 × 612 pts
    cx = pw / 2

    logo_size   = 90
    logo_margin = 50             # from page edge — equals vertical padding inside footer
    logo_y      = 35             # bottom of logo from page bottom (equal top/bottom margin)
    text_gap    = 20             # gap between logo edge and adjacent text
    line_left   = logo_margin + logo_size + text_gap   # 110
    line_right  = pw - line_left                        # 682

    pdf = canvas.Canvas(str(output_path), pagesize=landscape(letter))
    pdf.setTitle('Participation Certificate')

    # ── Parchment background ────────────────────────────────────────────
    pdf.setFillColor(PARCHMENT)
    pdf.rect(0, 0, pw, ph, fill=1, stroke=0)

    # ── Double border (plain rectangles, no corner decoration) ──────────
    m_out, m_in = 18, 30

    pdf.setStrokeColor(GARNET)
    pdf.setLineWidth(2.5)
    pdf.rect(m_out, m_out, pw - 2 * m_out, ph - 2 * m_out, fill=0, stroke=1)

    pdf.setLineWidth(0.8)
    pdf.rect(m_in, m_in, pw - 2 * m_in, ph - 2 * m_in, fill=0, stroke=1)

    # ── Title block ─────────────────────────────────────────────────────
    pdf.setFillColor(GARNET)
    pdf.setFont('LibreBaskerville-Bold', 28)
    pdf.drawCentredString(cx, 530, 'ACM at FSU Programming Contest')

    pdf.setFont('LibreBaskerville', 17)
    pdf.drawCentredString(cx, 498, 'Participant')

    # Separator below "Participant" — same span as footer separator
    pdf.setStrokeColor(GARNET)
    pdf.setLineWidth(0.6)
    pdf.line(line_left, 485, line_right, 485)

    pdf.setFont('LibreBaskerville', 13)
    pdf.drawCentredString(cx, 464, 'This certificate is awarded to')

    # ── Contestant name (MonteCarlo, 44 pt, slightly lower) ─────────────
    pdf.setFillColor(black)
    name = user.get_full_name() or user.username
    name_font, name_size = 'MonteCarlo', 44
    pdf.setFont(name_font, name_size)
    pdf.drawCentredString(cx, 413, name)
    name_w = stringWidth(name, name_font, name_size)
    pdf.setStrokeColor(black)
    pdf.setLineWidth(1.0)
    pdf.line(cx - name_w / 2, 399, cx + name_w / 2, 399)   # underline clear of script descenders

    footer_sep_y = 108
    detail_gap   = 26
    name_y       = 413
    placement_y  = round((2 * name_y + footer_sep_y + 2 * detail_gap) / 3)

    pdf.setFillColor(GARNET)
    pdf.setFont('LibreBaskerville', 13)
    pdf.drawCentredString(cx, placement_y + 38, 'for obtaining')

    placement   = _get_placement(team)
    placement_text = f'{_ordinal(placement)} Place' if placement else 'N/A'
    pdf.setFillColor(GARNET)
    pdf.setFont('LibreBaskerville-Bold', 32)
    pdf.drawCentredString(cx, placement_y, placement_text)

    pdf.setFont('LibreBaskerville', 13)
    pdf.drawCentredString(cx, placement_y - 26, f'in the {semester} Programming Contest')

    # ── Questions Answered - Team ────────────────────────────
    # Vertically centred between placement baseline and footer separator
    detail_center = (placement_y + footer_sep_y) / 2

    pdf.setFillColor(black)
    pdf.setFont('LibreBaskerville', 15)
    pdf.drawCentredString(cx, detail_center, f'Team: {team.name}')
    pdf.drawCentredString(cx, detail_center - detail_gap, f'Questions Answered: {team.questions_answered}')

    # ── Footer separator — same length as the "Participant" line above ───
    pdf.setStrokeColor(GARNET)
    pdf.setLineWidth(0.8)
    pdf.line(line_left, footer_sep_y, line_right, footer_sep_y)

    # ── Footer: [FSU logo] date (left)   right-text [ACM logo] ──────────
    right_text = 'ACM Chapter at Florida State University'

    text_y = logo_y + logo_size // 2 - 4   # vertically centred on the logo

    if os.path.exists(_FSU_LOGO):
        pdf.drawImage(_FSU_LOGO, logo_margin, logo_y,
                      width=logo_size, height=logo_size,
                      preserveAspectRatio=True, mask='auto')

    pdf.setFillColor(GARNET)
    pdf.setFont('LibreBaskerville', 13)
    pdf.drawString(line_left, text_y, granted)             # left-aligned at line anchor

    pdf.drawRightString(line_right, text_y, right_text)    # right-aligned at line anchor

    if os.path.exists(_ACM_LOGO):
        pdf.drawImage(_ACM_LOGO, pw - logo_margin - logo_size + 17, logo_y + 10,
                      width=logo_size - 15, height=logo_size - 15,
                      preserveAspectRatio=True, mask='auto')

    pdf.showPage()
    pdf.save()

    return relative_path
