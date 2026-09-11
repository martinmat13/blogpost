import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  const { id } = req.query;

  if (req.method === 'POST') {
    const { author, body, postId } = req.body;
    if (!author || !body || !postId) return res.status(400).json({ error: 'Missing fields' });

    const newComment = {
      id: 'com_' + Date.now(),
      postId: postId,
      author: author.trim(),
      body: body.trim(),
      date: new Date().toISOString(),
      likes: 0
    };

    // Save to Redis
    await kv.rpush(`comments:${postId}`, JSON.stringify(newComment));
    
    // Also save to global backup list for CMS tracking
    await kv.rpush(`all_comments`, JSON.stringify(newComment));

    return res.status(200).json({ success: true, comment: newComment });
  } 
  
  if (req.method === 'PUT') {
    // Used for liking a specific comment
    const { commentId, postId } = req.body;
    const rawComments = (await kv.lrange(`comments:${postId}`, 0, -1)) || [];
    
    const updatedComments = rawComments.map(c => {
      let item = typeof c === 'string' ? JSON.parse(c) : c;
      if (item.id === commentId) {
        item.likes = (item.likes || 0) + 1;
      }
      return JSON.stringify(item);
    });

    await kv.del(`comments:${postId}`);
    for (let c of updatedComments) {
      await kv.rpush(`comments:${postId}`, c);
    }
    return res.status(200).json({ success: true });
  }

  // GET request
  const rawComments = (await kv.lrange(`comments:${id}`, 0, -1)) || [];
  const comments = rawComments.map(c => typeof c === 'string' ? JSON.parse(c) : c);
  return res.status(200).json({ comments });
}