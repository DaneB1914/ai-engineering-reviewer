function findUser(email) {
  return db.query(`SELECT * FROM users WHERE email = '${email}'`);
}
