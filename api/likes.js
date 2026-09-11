import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  const { id } = req.query;
  if (!id) return res.status(400).json({ error: 'Missing post ID' });

  if (req.method === 'POST') {
    const current = await kv.incr(`likes:${id}`);
    return res.status(200).json({ likes: current });
  } else {
    const current = (await kv.get(`likes:${id}`)) || 0;
    return res.status(200).json({ likes: Number(current) });
  }
}