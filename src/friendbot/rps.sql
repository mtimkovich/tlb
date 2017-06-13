drop table if exists rps;

create table rps (
    id integer primary key,
    name text unique,
    score integer default 0
);
