# frozen_string_literal: true

begin
  /(?<ruby_version>\d+\.\d+)/ =~ RUBY_VERSION
  require_relative "#{ruby_version}/min_html"
rescue LoadError
  require_relative "min_html.so"
end
