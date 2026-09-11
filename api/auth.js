export default function handler(req, res) {
  const redirectUri = `https://github.com/login/oauth/authorize?client_id=${process.env.OAUTH_GITHUB_CLIENT_ID}&scope=repo,user`;
  res.redirect(302, redirectUri);
}