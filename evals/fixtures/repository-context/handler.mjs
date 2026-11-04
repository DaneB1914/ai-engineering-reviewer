import { findUser } from './find-user.mjs';
export async function handleLookup(db, email) {
  const { rows } = await findUser(db, email);
  if (rows.length === 0) return { status: 404, body: null };
  return { status: 200, body: rows[0] };
}
