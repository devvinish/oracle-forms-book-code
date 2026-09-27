-- Creates the CAREWELL user of the book's sample schema. Run as a DBA in the pluggable database
-- (the book's lab: FORMSPDB). It asks for the password.
accept carewell_password char prompt 'Password for CAREWELL: ' hide
create user carewell identified by "&carewell_password"
  default tablespace users quota unlimited on users;
grant create session, create table, create view, create sequence, create procedure, create trigger,
      create type, create synonym to carewell;
