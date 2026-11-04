-- Product policy: email identities are exact and case-sensitive.
CREATE TABLE users (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email text COLLATE "C" NOT NULL UNIQUE
);
