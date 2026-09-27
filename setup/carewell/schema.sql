-- CareWell Clinic: the sample schema of "Oracle Forms 14c: The Complete Developer's Guide".
-- Run as CAREWELL (see install.sql). Keys come from sequences, as in most Forms applications,
-- so that the book can show the PRE-INSERT trigger that fetches them.

create sequence departments_seq start with 100;
create sequence doctors_seq start with 1000;
create sequence patients_seq start with 10000;
create sequence appointments_seq start with 50000;
create sequence visits_seq start with 70000;
create sequence prescriptions_seq start with 90000;
create sequence invoices_seq start with 3000;
create sequence payments_seq start with 6000;
create sequence medicines_seq start with 500;

create table departments (
  dept_id      number(6)     constraint departments_pk primary key,
  dept_name    varchar2(40)  not null constraint departments_name_uk unique,
  floor_no     number(2)     not null,
  phone_ext    varchar2(6),
  head_doctor  number(6)
);
comment on table departments is 'Clinical departments of CareWell Clinic';

create table doctors (
  doctor_id    number(6)     constraint doctors_pk primary key,
  first_name   varchar2(30)  not null,
  last_name    varchar2(30)  not null,
  dept_id      number(6)     not null constraint doctors_dept_fk references departments,
  specialty    varchar2(40)  not null,
  phone        varchar2(20),
  email        varchar2(60),
  hire_date    date          not null,
  consult_fee  number(7,2)   not null constraint doctors_fee_ck check (consult_fee >= 0),
  active       varchar2(1)   default 'Y' not null constraint doctors_active_ck check (active in ('Y','N'))
);
alter table departments add constraint departments_head_fk foreign key (head_doctor) references doctors;

create table insurance_plans (
  plan_id       number(4)    constraint insurance_plans_pk primary key,
  provider      varchar2(40) not null,
  plan_name     varchar2(40) not null,
  coverage_pct  number(3)    not null constraint insurance_cov_ck check (coverage_pct between 0 and 100)
);

create table patients (
  patient_id    number(8)     constraint patients_pk primary key,
  mrn           varchar2(10)  not null constraint patients_mrn_uk unique,
  first_name    varchar2(30)  not null,
  last_name     varchar2(30)  not null,
  gender        varchar2(1)   not null constraint patients_gender_ck check (gender in ('F','M','X')),
  birth_date    date          not null,
  blood_group   varchar2(3)   constraint patients_blood_ck check (blood_group in ('A+','A-','B+','B-','AB+','AB-','O+','O-')),
  phone         varchar2(20),
  email         varchar2(60),
  address       varchar2(80),
  city          varchar2(30),
  plan_id       number(4)     constraint patients_plan_fk references insurance_plans,
  allergies     varchar2(200),
  photo         blob,
  registered_on date          default sysdate not null
);

create table rooms (
  room_no    varchar2(6)   constraint rooms_pk primary key,
  dept_id    number(6)     not null constraint rooms_dept_fk references departments,
  room_type  varchar2(12)  not null constraint rooms_type_ck check (room_type in ('CONSULT','PROCEDURE','LAB','WARD'))
);

create table appointments (
  appt_id       number(8)     constraint appointments_pk primary key,
  patient_id    number(8)     not null constraint appointments_patient_fk references patients,
  doctor_id     number(6)     not null constraint appointments_doctor_fk references doctors,
  appt_start    date          not null,
  duration_min  number(3)     default 15 not null constraint appointments_dur_ck check (duration_min between 5 and 240),
  room_no       varchar2(6)   constraint appointments_room_fk references rooms,
  status        varchar2(10)  default 'BOOKED' not null
                constraint appointments_status_ck check (status in ('BOOKED','CHECKED_IN','COMPLETED','CANCELLED','NO_SHOW')),
  reason        varchar2(100)
);

create table visits (
  visit_id       number(8)      constraint visits_pk primary key,
  appt_id        number(8)      constraint visits_appt_fk references appointments,
  patient_id     number(8)      not null constraint visits_patient_fk references patients,
  doctor_id      number(6)      not null constraint visits_doctor_fk references doctors,
  visit_date     date           not null,
  symptoms       varchar2(200),
  diagnosis      varchar2(200),
  notes          varchar2(2000),
  temperature_c  number(4,1),
  bp_systolic    number(3),
  bp_diastolic   number(3),
  follow_up_on   date
);

create table medicine_categories (
  category_id    number(4)     constraint medicine_categories_pk primary key,
  parent_id      number(4)     constraint medicine_categories_parent_fk references medicine_categories,
  category_name  varchar2(40)  not null
);

create table medicines (
  medicine_id    number(6)     constraint medicines_pk primary key,
  category_id    number(4)     not null constraint medicines_category_fk references medicine_categories,
  medicine_name  varchar2(40)  not null,
  dosage_form    varchar2(12)  not null constraint medicines_form_ck check (dosage_form in ('TABLET','CAPSULE','SYRUP','INJECTION','CREAM','DROPS','INHALER')),
  strength       varchar2(20),
  unit_price     number(8,2)   not null,
  stock_qty      number(6)     default 0 not null,
  reorder_level  number(6)     default 20 not null
);

create table prescriptions (
  rx_id        number(8)     constraint prescriptions_pk primary key,
  visit_id     number(8)     not null constraint prescriptions_visit_fk references visits on delete cascade,
  medicine_id  number(6)     not null constraint prescriptions_medicine_fk references medicines,
  dosage       varchar2(30)  not null,
  frequency    varchar2(20)  not null,
  days         number(3)     not null constraint prescriptions_days_ck check (days > 0),
  quantity     number(4)     not null constraint prescriptions_qty_ck check (quantity > 0)
);

create table invoices (
  invoice_id    number(8)     constraint invoices_pk primary key,
  visit_id      number(8)     constraint invoices_visit_fk references visits,
  patient_id    number(8)     not null constraint invoices_patient_fk references patients,
  invoice_date  date          not null,
  status        varchar2(8)   default 'OPEN' not null constraint invoices_status_ck check (status in ('OPEN','PARTIAL','PAID','VOID')),
  total_amount  number(10,2)  default 0 not null
);

create table invoice_lines (
  invoice_id   number(8)     not null constraint invoice_lines_invoice_fk references invoices on delete cascade,
  line_no      number(3)     not null,
  description  varchar2(60)  not null,
  quantity     number(5)     default 1 not null,
  unit_price   number(8,2)   not null,
  constraint invoice_lines_pk primary key (invoice_id, line_no)
);

create table payments (
  payment_id  number(8)     constraint payments_pk primary key,
  invoice_id  number(8)     not null constraint payments_invoice_fk references invoices,
  paid_on     date          not null,
  amount      number(10,2)  not null constraint payments_amount_ck check (amount > 0),
  method      varchar2(10)  not null constraint payments_method_ck check (method in ('CASH','CARD','INSURANCE','UPI'))
);

create table app_users (
  username   varchar2(30)  constraint app_users_pk primary key,
  full_name  varchar2(60)  not null,
  app_role   varchar2(20)  not null constraint app_users_role_ck check (app_role in ('ADMIN','DOCTOR','RECEPTION','BILLING','PHARMACY')),
  doctor_id  number(6)     constraint app_users_doctor_fk references doctors,
  active     varchar2(1)   default 'Y' not null
);

create table audit_log (
  audit_id    number        generated always as identity constraint audit_log_pk primary key,
  table_name  varchar2(30)  not null,
  row_key     varchar2(40)  not null,
  action      varchar2(10)  not null,
  changed_by  varchar2(30)  default user not null,
  changed_on  date          default sysdate not null,
  details     varchar2(400)
);

create index doctors_dept_ix on doctors (dept_id);
create index patients_name_ix on patients (last_name, first_name);
create index appointments_patient_ix on appointments (patient_id);
create index appointments_doctor_ix on appointments (doctor_id, appt_start);
create index visits_patient_ix on visits (patient_id);
create index prescriptions_visit_ix on prescriptions (visit_id);
create index invoices_patient_ix on invoices (patient_id);
create index payments_invoice_ix on payments (invoice_id);

-- the invoice total follows its lines (and the book shows the same in a form, with a summary item)
create or replace view invoice_totals as
  select i.invoice_id, i.patient_id, i.invoice_date, i.status,
         nvl(sum(l.quantity * l.unit_price), 0) as lines_total,
         (select nvl(sum(p.amount), 0) from payments p where p.invoice_id = i.invoice_id) as paid
  from   invoices i left join invoice_lines l on l.invoice_id = i.invoice_id
  group  by i.invoice_id, i.patient_id, i.invoice_date, i.status;
