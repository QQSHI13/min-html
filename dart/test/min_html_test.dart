import 'package:min_html/min_html.dart';
import 'package:test/test.dart';

void main() {
  test("should minify html", () {
    expect(
      minifyHtml("<p>  Hello World!   </p>"),
      "<p>Hello World!",
    );
  });
}
