drop table if exists employees;
create table employees (
        user_id integer primary key autoincrement,
        user_name text not null,
        user_last text not null,
	user_dep text not null
);
