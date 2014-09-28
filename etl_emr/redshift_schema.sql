CREATE TABLE events(
ev_date      DATE NOT NULL,
client_key   VARCHAR(100),
client_ip    VARCHAR(50),
uid          VARCHAR(100),
sid          VARCHAR(100),
content_type VARCHAR(50),
client_host  VARCHAR(100),
client_url   VARCHAR(100),
content_host VARCHAR(100),
content_url  VARCHAR(100),
user_os      VARCHAR(100),
user_browser VARCHAR(100),
row_count    int,
activity     VARCHAR(50),
act_count    int,
act_len      int
);

CREATE TABLE events_agg_video(
ev_date      DATE NOT NULL,
client_host  VARCHAR(100),
content_host VARCHAR(100),
content_url  VARCHAR(100),
view_count   int,
hover_count  int,
play_count   int,
play_length  int
);
