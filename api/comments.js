import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  const { id } = req.query;
  if (!id) return res.status(400).json({ error: 'Missing post ID' });

  if (req.method === 'POST') {
    const { author, body } = req.body;
    if (!author || !body) return res.status(400).json({ error: 'Missing fields' });

    const newComment = {
      author: author.trim(),
      body: body.trim(),
      date: new Date().toISOString()
    };

    await kv.rpush(`comments:${id}`, JSON.stringify(newComment));
    return res.status(200).json({ success: true, comment: newComment });
  } else {
    const rawComments = (await kv.lrange(`comments:${id}`, 0, -1)) || [];
    const comments = rawComments.map(c => typeof c === 'string' ? JSON.parse(c) : c);
    return res.status(200).json({ comments });
  }
}