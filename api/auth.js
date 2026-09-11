module.exports = (req, res) => {
  const redirectUri = `https://github.com/login/oauth/authorize?client_id=${process.env.Ov23ligntIF1htySGQFg}&scope=repo,user`;
  res.redirect(302, redirectUri);
};