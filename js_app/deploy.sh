rm -rf public
gulp build
cd public
git init
git add -A
git commit -m 'update cksdotcom'
git push -f git@github.com:ckeisato/cksdotcom.git master:gh-pages
