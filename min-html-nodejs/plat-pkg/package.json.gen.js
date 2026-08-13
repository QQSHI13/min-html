const {platform, arch} = {
  "aarch64-unknown-linux-gnu": {platform: "linux", arch: "arm64"},
  "x86_64-unknown-linux-gnu": {platform: "linux", arch: "x64"},
  "aarch64-apple-darwin": {platform: "darwin", arch: "arm64"},
  "x86_64-apple-darwin": {platform: "darwin", arch: "x64"},
  "x86_64-pc-windows-msvc": {platform: "win32", arch: "x64"},
}[process.env.TARGET];
const {version} = require("../package.json");
require("fs").writeFileSync(`${__dirname}/package.json`, JSON.stringify({
  name: `@min-html/node-${platform}-${arch}`,
  version,
  description: `@min-html/node native module build for ${platform}-${arch}`,
  main: "index.node",
  files: ["README.md", "index.node"],
  repository: {
    type: "git",
    url: "git+https://github.com/QQSHI13/min-html.git",
  },
  os: [platform],
  cpu: [arch],
}, null, 2));
