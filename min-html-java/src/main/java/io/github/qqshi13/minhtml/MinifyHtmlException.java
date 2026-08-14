package io.github.qqshi13.minhtml;

public class MinifyHtmlException extends RuntimeException {
  MinifyHtmlException(String message) {
    super(message);
  }

  MinifyHtmlException(String message, Throwable cause) {
    super(message, cause);
  }
}
