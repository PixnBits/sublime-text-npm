sublime-text-npm
================

npm commands within Sublime Text (v3)

[Git integration](https://github.com/kemayo/sublime-text-git) is handy, so why not [npm](https://www.npmjs.org/) too?

Installation
============
1. Install [Package Control](https://sublime.wbond.net/installation)
2. Open the "[Command Pallet](http://sublime-text-unofficial-documentation.readthedocs.org/en/latest/extensibility/command_palette.html#command-palette)" (<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> or <kbd>⌘</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd>)
3. type "pkgctlinspkg" (for "Package Control: Install Package" ;-)
4. type "[npm](https://sublime.wbond.net/packages/npm)"
5. Tah-dah!

Commands Implemented
====================
If you don't see your favorite here, please [file an issue](https://github.com/PixnBits/sublime-text-npm/issues).

[Install](https://www.npmjs.org/doc/cli/npm-install.html):
* Install Package: `npm install`
* Install and Save Package: `npm install --save`
* Install and Save Development Package: `npm install --save-dev`

[List](https://www.npmjs.org/doc/cli/npm-ls.html):
* List Installed Packages: `npm list --depth 0`
* List Installed Packages, Deep `npm list`

[Update](https://www.npmjs.org/doc/cli/npm-update.html)
* Update Local Packages: `npm update` or `npm update <name>`
