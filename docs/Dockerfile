FROM ruby:3.3

RUN gem install bundler

WORKDIR /usr/src/app

COPY Gemfile* .

RUN bundle install

COPY . .

EXPOSE 4000

ENTRYPOINT [ "bundle", "exec", "jekyll" ]
CMD [ "serve", "--host=0.0.0.0" ]
