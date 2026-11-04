export function findUser(db, email) {
  return db.query('SELECT id, email FROM users WHERE email = $1', [email]);
}
