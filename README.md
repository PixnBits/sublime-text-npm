sublime-text-npm
================

npm commands within Sublime Text (v3)

[Git integration](https://github.com/kemayo/sublime-text-git) is handy, so why not [npm](https://www.npmjs.org/) too?

Installation
============

1. Install [node and npm](http://nodejs.org/) on your machine
2. Install [Package Control](https://sublime.wbond.net/installation) in Sublime Text
3. Open the "[Command Pallet](http://sublime-text-unofficial-documentation.readthedocs.org/en/latest/extensibility/command_palette.html#command-palette)" (<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> or <kbd>⌘</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd>)
4. type "pkgctlinspkg" (for "Package Control: Install Package" ;-)
5. type "[npm](https://sublime.wbond.net/packages/npm)"
6. Tah-dah!

Usage
=====

1. Open a file (usually a *.js or *.coffee) in your npm project/package
2. <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> or <kbd>⌘</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd>
3. Type `npm: ` to see all npm commands
4. Press <kbd>Enter</kbd> to invoke the selected command. The npm command will be run in the directory of your focused file.

Commands Implemented
====================

If you don't see your favorite here, please [file an issue](https://github.com/PixnBits/sublime-text-npm/issues).

[Install](https://www.npmjs.org/doc/cli/npm-install.html):

* Install Saved Packages: `npm install`
* Install Package: `npm install <pkg name>`
* Install and Save Package: `npm install <pkg name> --save`
* Install and Save Development Package: `npm install <pkg name> --save-dev`

[Uninstall]():

* Remove/Uninstall Package: `npm rm`
* Remove/Uninstall Saved Package: `npm rm --save --save-dev -save-optional`

[List](https://www.npmjs.org/doc/cli/npm-ls.html):

* List Installed Packages: `npm list --depth 0`
* List Installed Packages, Deep: `npm list`

[Outdated](https://docs.npmjs.com/cli/outdated):

* Check for outdated packages: `npm outdated`

[Run](https://docs.npmjs.com/cli/run-script):

* Run Script: `npm run <script>`

[Update](https://www.npmjs.org/doc/cli/npm-update.html):

* Update Local Packages: `npm update` or `npm update <name>`

[Search](https://www.npmjs.org/doc/cli/npm-search.html):

* Search Packages: `npm search <name>`

[Link](https://www.npmjs.org/doc/cli/npm-link.html):

* Register this Package for Linking: `npm link`
* Link Package Here: `npm link <name>`

[Test](https://docs.npmjs.com/cli/test):

* Test a package: `npm test`

Run Arbitrary:

* Run something not covered here (basically, `npm <whatever your input was>`)
