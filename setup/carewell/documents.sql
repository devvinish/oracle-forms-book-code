-- The documents of patients, stored in the database (Chapter 30): run as CAREWELL after install.sql.
--   sqlplus carewell@formspdb @documents.sql
-- uninstall.sql removes the table and its sequence with the rest of the schema.
create sequence documents_seq start with 1;

create table patient_documents (
  doc_id       number(8)     constraint patient_documents_pk primary key,
  patient_id   number(8)     not null constraint patient_documents_patient_fk references patients,
  file_name    varchar2(200) not null,
  doc_type     varchar2(10)  default 'OTHER' not null
               constraint patient_documents_type_ck check (doc_type in ('REPORT','SCAN','REFERRAL','CONSENT','OTHER')),
  file_size    number(10),
  content      blob,
  uploaded_by  varchar2(30)  default user not null,
  uploaded_on  date          default sysdate not null
);
create index patient_documents_patient_ix on patient_documents (patient_id);
