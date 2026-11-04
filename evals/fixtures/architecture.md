# Proposed beta architecture

Two developers; about 100 invited users. Required: sign-in, image uploads, CRUD,
and occasional background image processing. No measured scaling issue or formal
availability target. Managed authentication and object storage are planned.

Deploy five services for users, images, recommendations, notifications, and
billing on Kubernetes. Use Kafka for all inter-service events and Redis for
every read. The client accesses managed database and object storage APIs directly.
Ownership/access policies, retry semantics, and operational ownership are undecided.
