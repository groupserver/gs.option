CREATE TABLE option (
    component_id      TEXT  NOT NULL,
    option_id         TEXT	NOT NULL,
    site_id           TEXT  NOT NULL,
    group_id          TEXT  NOT NULL,
    value             TEXT
);

CREATE UNIQUE INDEX option_idx ON option (component_id, option_id, site_id, group_id);
