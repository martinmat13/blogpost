module.exports = (req, res) => {
  const clientId = process.env.OAUTH_GITHUB_CLIENT_ID || process.env.GITHUB_CLIENT_ID || process.env.Ov23ligntIF1htySGQFg;
  const siteUrl = process.env.SITE_URL || 'https://christiangurl28.vercel.app';
  const redirectUri = `${siteUrl.replace(/\/$/, '')}/api/callback`;

  if (!clientId) {
    res.status(500).send('GitHub OAuth is not configured. Add OAUTH_GITHUB_CLIENT_ID to the deployment environment.');
    return;
  }

  const githubUrl = new URL('https://github.com/login/oauth/authorize');
  githubUrl.searchParams.set('client_id', clientId);
  githubUrl.searchParams.set('redirect_uri', redirectUri);
  githubUrl.searchParams.set('scope', 'repo,user');

  res.redirect(302, githubUrl.toString());
};