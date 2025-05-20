--changeset abhinav.srikanth:1747653901222-1
CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

--changeset abhinav.srikanth:1747653901222-2
CREATE TABLE auth_group_permissions (
    id BIGSERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL
);

--changeset abhinav.srikanth:1747653901222-3
CREATE TABLE auth_user_groups (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL
);

--changeset abhinav.srikanth:1747653901222-4
CREATE TABLE auth_user_user_permissions (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL
);

--changeset abhinav.srikanth:1747653901222-5
CREATE TABLE django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER,
    user_id INTEGER NOT NULL
);

--changeset abhinav.srikanth:1747653901222-6
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

--changeset abhinav.srikanth:1747653901222-7
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

--changeset abhinav.srikanth:1747653901222-8
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

--changeset abhinav.srikanth:1747653901222-9
CREATE TABLE config_metas (
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    parent_question_operator VARCHAR(255),
    siac_id VARCHAR(255),
    default_option VARCHAR(255),
    parent_response_condition JSONB,
    possible_options VARCHAR,
    enable_task_response VARCHAR(255),
    entity_type VARCHAR(255),
    parent_option_condition JSONB,
    question_type VARCHAR(255),
    attributes JSONB,
    state_id INTEGER,
    question_id INTEGER,
    job_id INTEGER,
    task_id INTEGER,
    category VARCHAR(255),
    is_active BOOLEAN,
    id VARCHAR(100) NOT NULL,
    config_id VARCHAR(255) NOT NULL PRIMARY KEY,
    skip_trigger BOOLEAN DEFAULT FALSE
);

--changeset abhinav.srikanth:1747653901222-10
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);

--changeset abhinav.srikanth:1747653901222-11
CREATE INDEX auth_permission_content_type_id_2f476e4b ON auth_permission(content_type_id);

--changeset abhinav.srikanth:1747653901222-12
ALTER TABLE auth_permission ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);

--changeset abhinav.srikanth:1747653901222-13
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON auth_group_permissions(group_id);

--changeset abhinav.srikanth:1747653901222-14
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON auth_group_permissions(permission_id);

--changeset abhinav.srikanth:1747653901222-15
ALTER TABLE auth_group_permissions ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);

--changeset abhinav.srikanth:1747653901222-16
CREATE INDEX auth_user_groups_user_id_6a12ed8b ON auth_user_groups(user_id);

--changeset abhinav.srikanth:1747653901222-17
CREATE INDEX auth_user_groups_group_id_97559544 ON auth_user_groups(group_id);

--changeset abhinav.srikanth:1747653901222-18
ALTER TABLE auth_user_groups ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);

--changeset abhinav.srikanth:1747653901222-19
CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON auth_user_user_permissions(user_id);

--changeset abhinav.srikanth:1747653901222-20
CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON auth_user_user_permissions(permission_id);

--changeset abhinav.srikanth:1747653901222-21
ALTER TABLE auth_user_user_permissions ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);

--changeset abhinav.srikanth:1747653901222-22
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log(content_type_id);

--changeset abhinav.srikanth:1747653901222-23
CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log(user_id);

--changeset abhinav.srikanth:1747653901222-24
ALTER TABLE auth_user ADD CONSTRAINT auth_user_username_key UNIQUE (username);

--changeset abhinav.srikanth:1747653901222-25
ALTER TABLE auth_group ADD CONSTRAINT auth_group_name_key UNIQUE (name);

--changeset abhinav.srikanth:1747653901222-26
CREATE INDEX django_session_expire_date_a5c62663 ON django_session(expire_date);

--changeset abhinav.srikanth:1747653901222-27
ALTER TABLE django_content_type ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);

--changeset abhinav.srikanth:1747653901222-28
CREATE TABLE django_migrations (
    id BIGSERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);

--changeset abhinav.srikanth:1747653901222-29
CREATE TABLE job_master (
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    job_name VARCHAR(255),
    conditions JSONB,
    order_id INTEGER,
    job_id INTEGER NOT NULL PRIMARY KEY,
    job_type VARCHAR(255),
    system_identifier VARCHAR(255)
);

--changeset abhinav.srikanth:1747653901222-30
CREATE TABLE question_master (
    question_id INTEGER NOT NULL PRIMARY KEY,
    attributes JSONB,
    created_at TIMESTAMP,
    default_option VARCHAR(255),
    identifier VARCHAR(255),
    is_active BOOLEAN,
    is_master BOOLEAN,
    is_multi_select BOOLEAN,
    order_id INTEGER,
    possible_options VARCHAR,
    question_name VARCHAR(255),
    source_category VARCHAR(255),
    ui_element_type VARCHAR(255),
    updated_at TIMESTAMP
);

--changeset abhinav.srikanth:1747653901222-31
CREATE TABLE siac_master (
    siac_id VARCHAR(255) NOT NULL PRIMARY KEY,
    conditions JSONB,
    created_at TIMESTAMP,
    description VARCHAR(255),
    scheme VARCHAR(255),
    sector VARCHAR(255),
    siac_uuid UUID,
    updated_at TIMESTAMP
);

--changeset abhinav.srikanth:1747653901222-32
CREATE TABLE state_master (
    state_id INTEGER NOT NULL PRIMARY KEY,
    condition JSONB,
    created_at TIMESTAMP,
    description VARCHAR(255),
    state_name VARCHAR(255),
    system_identifier VARCHAR(255),
    updated_at TIMESTAMP
);

--changeset abhinav.srikanth:1747653901222-33
CREATE TABLE task_master (
    mandatory BOOLEAN NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    task_name VARCHAR(255),
    conditions JSONB,
    order_id INTEGER,
    task_type VARCHAR(255),
    task_id INTEGER NOT NULL PRIMARY KEY,
    system_identifier VARCHAR(255)
);

--changeset abhinav.srikanth:1747653901222-34
ALTER TABLE auth_group_permissions ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-35
ALTER TABLE auth_group_permissions ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-36
ALTER TABLE auth_permission ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-37
ALTER TABLE auth_user_groups ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-38
ALTER TABLE auth_user_groups ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-39
ALTER TABLE auth_user_user_permissions ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-40
ALTER TABLE auth_user_user_permissions ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-41
ALTER TABLE django_admin_log ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747653901222-42
ALTER TABLE django_admin_log ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;

--changeset abhinav.srikanth:1747737177000-43
ALTER TABLE config_metas ALTER COLUMN enable_task_response TYPE VARCHAR(255) USING enable_task_response::text;