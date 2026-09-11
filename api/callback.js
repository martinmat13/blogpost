module.exports = async (req, res) => {
  const { code, error, error_description: errorDescription } = req.query;
  const clientId = process.env.OAUTH_GITHUB_CLIENT_ID || process.env.GITHUB_CLIENT_ID || process.env.Ov23ligntIF1htySGQFg;
  const clientSecret = process.env.OAUTH_GITHUB_CLIENT_SECRET || process.env.GITHUB_CLIENT_SECRET;
  const siteUrl = process.env.SITE_URL || 'https://christiangurl28.vercel.app';
  const redirectUri = `${siteUrl.replace(/\/$/, '')}/api/callback`;

  if (error) {
    res.status(400).send(`GitHub login was cancelled: ${errorDescription || error}`);
    return;
  }

  if (!code || !clientId || !clientSecret) {
    res.status(500).send('GitHub OAuth is not configured correctly. Check the deployment environment variables.');
    return;
  }

  try {
    const response = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code: code,
        redirect_uri: redirectUri,
      }),
    });

    const data = await response.json();
    if (!data.access_token) {
      res.status(502).send(`GitHub did not issue an access token: ${data.error_description || data.error || 'unknown error'}`);
      return;
    }

    const token = data.access_token;

    const script = `
      <script>
        const receiveMessage = (message) => {
          window.opener.postMessage(
            'authorization:github:success:${JSON.stringify({ token, provider: 'github' })}',
            message.origin
          );
          window.removeEventListener('message', receiveMessage, false);
        }
        window.addEventListener('message', receiveMessage, false);
        window.opener.postMessage('authorizing:github', '*');
      </script>
    `;
    res.status(200).send(script);
  } catch (err) {
    res.status(500).send('Authentication failed.');
  }
};