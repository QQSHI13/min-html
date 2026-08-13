use crate::ast::AttrVal;
use crate::ast::ElementClosingTag;
use crate::ast::NodeData;
use crate::parse::element::parse_element;
use crate::parse::element::parse_tag;
use crate::parse::element::ParsedTag;
use crate::parse::Code;
use ahash::AHashMap;
use minify_html_common::spec::tag::ns::Namespace;
use minify_html_common::spec::tag::EMPTY_SLICE;

fn val(v: &[u8]) -> AttrVal {
  AttrVal {
    value: v.to_vec(),
    quote: None,
  }
}

#[test]
fn test_parse_tag() {
  let mut code = Code::new(
    br###"<input type


				 =
			"password"  "a"  = "  b  "   :cd  /e /=fg 	= /\h /i/ /j/k/l m=n=o q==\r/s/ / t] = /u  / w=//>"###,
  );
  let tag = parse_tag(&mut code, Namespace::Html);
  assert_eq!(tag, ParsedTag {
    attributes: {
      let mut map = AHashMap::<Vec<u8>, AttrVal>::default();
      map.insert(b"type".to_vec(), val(b"password"));
      map.insert(b"\"a\"".to_vec(), val(b"  b  "));
      map.insert(b":cd".to_vec(), val(b""));
      map.insert(b"e".to_vec(), val(b""));
      map.insert(b"=fg".to_vec(), val(b"/\\h"));
      map.insert(b"i".to_vec(), val(b""));
      map.insert(b"j".to_vec(), val(b""));
      map.insert(b"k".to_vec(), val(b""));
      map.insert(b"l".to_vec(), val(b""));
      map.insert(b"m".to_vec(), val(b"n=o"));
      map.insert(b"q".to_vec(), val(b"=\\r/s/"));
      map.insert(b"t]".to_vec(), val(b"/u"));
      map.insert(b"w".to_vec(), val(b"//"));
      map
    },
    name: b"input".to_vec(),
    self_closing: false,
  });
}

#[test]
fn test_parse_svg_preserves_case() {
  // SVG is foreign content: element and attribute names are case-sensitive.
  let mut code = Code::new(
    br###"<svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid"><linearGradient></linearGradient></svg>"###,
  );
  let elem = parse_element(&mut code, Namespace::Html, EMPTY_SLICE);
  let NodeData::Element {
    attributes,
    children,
    name,
    namespace,
    ..
  } = elem
  else {
    panic!("expected element");
  };
  assert_eq!(name, b"svg".to_vec());
  assert_eq!(namespace, Namespace::Svg);
  assert!(attributes.contains_key(b"viewBox".as_ref()));
  assert!(attributes.contains_key(b"preserveAspectRatio".as_ref()));
  assert!(!attributes.contains_key(b"viewbox".as_ref()));
  let NodeData::Element {
    name, namespace, ..
  } = &children[0]
  else {
    panic!("expected child element");
  };
  assert_eq!(name.as_slice(), b"linearGradient");
  assert_eq!(*namespace, Namespace::Svg);
}

#[test]
fn test_parse_element() {
  let mut code = Code::new(br#"<a b=\"c\"></a>"#);
  let elem = parse_element(&mut code, Namespace::Html, EMPTY_SLICE);
  assert_eq!(elem, NodeData::Element {
    attributes: {
      let mut map = AHashMap::<Vec<u8>, AttrVal>::default();
      map.insert(b"b".to_vec(), val(br#"\"c\""#));
      map
    },
    children: vec![],
    closing_tag: ElementClosingTag::Present,
    name: b"a".to_vec(),
    namespace: Namespace::Html,
    next_sibling_element_name: Vec::new(),
  });
}
