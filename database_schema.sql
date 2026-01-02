-- ============================================================================
-- MKP Operational System Factory - Database Schema (DDL)
-- ============================================================================
-- Database: PostgreSQL
-- Description: Complete database schema for MKP Operational System Factory
-- Version: 2.0 (includes password column in workers table)
-- ============================================================================

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS production_log_problem_comments CASCADE;
DROP TABLE IF EXISTS production_logs CASCADE;
DROP TABLE IF EXISTS workers CASCADE;
DROP TABLE IF EXISTS sub_positions CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS shifts CASCADE;
DROP TABLE IF EXISTS problem_comments CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS positions CASCADE;
DROP TABLE IF EXISTS divisions CASCADE;

-- Drop sequences if they exist
DROP SEQUENCE IF EXISTS departments_id_seq CASCADE;
DROP SEQUENCE IF EXISTS divisions_id_seq CASCADE;
DROP SEQUENCE IF EXISTS items_id_seq CASCADE;
DROP SEQUENCE IF EXISTS positions_id_seq CASCADE;
DROP SEQUENCE IF EXISTS problem_comments_id_seq CASCADE;
DROP SEQUENCE IF EXISTS production_log_problem_comments_id_seq CASCADE;
DROP SEQUENCE IF EXISTS production_logs_id_seq CASCADE;
DROP SEQUENCE IF EXISTS shifts_id_seq CASCADE;
DROP SEQUENCE IF EXISTS sub_positions_id_seq CASCADE;
DROP SEQUENCE IF EXISTS suppliers_id_seq CASCADE;
DROP SEQUENCE IF EXISTS workers_id_seq CASCADE;

-- ============================================================================
-- CREATE SEQUENCES
-- ============================================================================

CREATE SEQUENCE divisions_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE departments_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE positions_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE sub_positions_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE workers_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE shifts_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE suppliers_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE items_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE problem_comments_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE production_logs_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1
    NO CYCLE;

CREATE SEQUENCE production_log_problem_comments_id_seq
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 2147483647
    START 1
    CACHE 1
    NO CYCLE;

-- ============================================================================
-- CREATE TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Table: divisions
-- Description: Divisi dalam organisasi (e.g., Kawat, IT)
-- ----------------------------------------------------------------------------
CREATE TABLE divisions (
    id INTEGER NOT NULL DEFAULT nextval('divisions_id_seq'::regclass),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT divisions_pkey PRIMARY KEY (id),
    CONSTRAINT divisions_code_key UNIQUE (code),
    CONSTRAINT divisions_name_key UNIQUE (name)
);

ALTER SEQUENCE divisions_id_seq OWNED BY divisions.id;

-- ----------------------------------------------------------------------------
-- Table: departments
-- Description: Departemen dalam divisi (e.g., Operator, Koordinator, Supervisor)
-- ----------------------------------------------------------------------------
CREATE TABLE departments (
    id INTEGER NOT NULL DEFAULT nextval('departments_id_seq'::regclass),
    division_id INTEGER NOT NULL,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT departments_pkey PRIMARY KEY (id),
    CONSTRAINT departments_division_code_unique UNIQUE (division_id, code),
    CONSTRAINT departments_division_id_fkey FOREIGN KEY (division_id)
        REFERENCES divisions(id) ON DELETE RESTRICT
);

ALTER SEQUENCE departments_id_seq OWNED BY departments.id;

-- ----------------------------------------------------------------------------
-- Table: positions
-- Description: Posisi pekerjaan (e.g., PER, RAM, TEMBAK, POCKET, ASSEMBLY, FRAME, SUPPLY)
-- ----------------------------------------------------------------------------
CREATE TABLE positions (
    id INTEGER NOT NULL DEFAULT nextval('positions_id_seq'::regclass),
    code VARCHAR(20) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    CONSTRAINT positions_pkey PRIMARY KEY (id),
    CONSTRAINT positions_code_key UNIQUE (code),
    CONSTRAINT positions_unit_check CHECK (unit IN ('pcs', 'lmbr'))
);

ALTER SEQUENCE positions_id_seq OWNED BY positions.id;

-- ----------------------------------------------------------------------------
-- Table: sub_positions
-- Description: Sub posisi atau mesin dalam posisi (e.g., FC60, SX80, MEJA-1)
-- ----------------------------------------------------------------------------
CREATE TABLE sub_positions (
    id INTEGER NOT NULL DEFAULT nextval('sub_positions_id_seq'::regclass),
    position_id INTEGER NOT NULL,
    code VARCHAR(30) NOT NULL,
    CONSTRAINT sub_positions_pkey PRIMARY KEY (id),
    CONSTRAINT sub_positions_position_id_code_key UNIQUE (position_id, code),
    CONSTRAINT sub_positions_position_id_fkey FOREIGN KEY (position_id)
        REFERENCES positions(id) ON DELETE RESTRICT
);

ALTER SEQUENCE sub_positions_id_seq OWNED BY sub_positions.id;

-- ----------------------------------------------------------------------------
-- Table: workers
-- Description: Pekerja/operator dalam sistem
-- ----------------------------------------------------------------------------
CREATE TABLE workers (
    id INTEGER NOT NULL DEFAULT nextval('workers_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255),
    position_id INTEGER,
    department_id INTEGER,
    CONSTRAINT workers_pkey PRIMARY KEY (id),
    CONSTRAINT workers_position_id_fkey FOREIGN KEY (position_id)
        REFERENCES positions(id) ON DELETE RESTRICT,
    CONSTRAINT workers_department_id_fkey FOREIGN KEY (department_id)
        REFERENCES departments(id) ON DELETE RESTRICT
);

ALTER SEQUENCE workers_id_seq OWNED BY workers.id;

-- ----------------------------------------------------------------------------
-- Table: shifts
-- Description: Shift kerja (e.g., Shift 1, Shift 2, Shift 3)
-- ----------------------------------------------------------------------------
CREATE TABLE shifts (
    id INTEGER NOT NULL DEFAULT nextval('shifts_id_seq'::regclass),
    name VARCHAR(20) NOT NULL,
    CONSTRAINT shifts_pkey PRIMARY KEY (id),
    CONSTRAINT shifts_name_key UNIQUE (name)
);

ALTER SEQUENCE shifts_id_seq OWNED BY shifts.id;

-- ----------------------------------------------------------------------------
-- Table: suppliers
-- Description: Supplier material (e.g., Intiroda, Mega, Kingdom)
-- ----------------------------------------------------------------------------
CREATE TABLE suppliers (
    id INTEGER NOT NULL DEFAULT nextval('suppliers_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    CONSTRAINT suppliers_pkey PRIMARY KEY (id),
    CONSTRAINT suppliers_name_key UNIQUE (name)
);

ALTER SEQUENCE suppliers_id_seq OWNED BY suppliers.id;

-- ----------------------------------------------------------------------------
-- Table: items
-- Description: Item produk yang diproduksi
-- ----------------------------------------------------------------------------
CREATE TABLE items (
    id INTEGER NOT NULL DEFAULT nextval('items_id_seq'::regclass),
    item_number VARCHAR(50) NOT NULL,
    item_name VARCHAR(100),
    spec TEXT,
    CONSTRAINT items_pkey PRIMARY KEY (id),
    CONSTRAINT items_item_number_key UNIQUE (item_number)
);

ALTER SEQUENCE items_id_seq OWNED BY items.id;

-- ----------------------------------------------------------------------------
-- Table: problem_comments
-- Description: Komentar atau jenis kendala produksi
-- ----------------------------------------------------------------------------
CREATE TABLE problem_comments (
    id INTEGER NOT NULL DEFAULT nextval('problem_comments_id_seq'::regclass),
    description VARCHAR(255) NOT NULL,
    CONSTRAINT problem_comments_pkey PRIMARY KEY (id),
    CONSTRAINT problem_comments_description_key UNIQUE (description)
);

ALTER SEQUENCE problem_comments_id_seq OWNED BY problem_comments.id;

-- ----------------------------------------------------------------------------
-- Table: production_logs
-- Description: Log produksi harian
-- ----------------------------------------------------------------------------
CREATE TABLE production_logs (
    id BIGINT NOT NULL DEFAULT nextval('production_logs_id_seq'::regclass),
    worker_id INTEGER NOT NULL,
    position_id INTEGER NOT NULL,
    sub_position_id INTEGER,
    shift_id INTEGER NOT NULL,
    supplier_id INTEGER,
    item_id INTEGER NOT NULL,
    qty_output NUMERIC(10, 2) NOT NULL,
    qty_reject NUMERIC(10, 2) NOT NULL,
    problem_duration_minutes INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_coordinator BOOLEAN,
    approved_spv BOOLEAN,
    approved_coordinator_at TIMESTAMP,
    approved_spv_at TIMESTAMP,
    approved_coordinator_by INTEGER,
    approved_spv_by INTEGER,
    CONSTRAINT production_logs_pkey PRIMARY KEY (id),
    CONSTRAINT production_logs_problem_duration_minutes_check CHECK (problem_duration_minutes >= 0),
    CONSTRAINT production_logs_qty_output_check CHECK (qty_output >= 0),
    CONSTRAINT production_logs_qty_reject_check CHECK (qty_reject >= 0),
    CONSTRAINT spv_after_coordinator_check CHECK ((approved_spv IS NULL) OR (approved_coordinator = true)),
    CONSTRAINT production_logs_worker_id_fkey FOREIGN KEY (worker_id)
        REFERENCES workers(id),
    CONSTRAINT production_logs_position_id_fkey FOREIGN KEY (position_id)
        REFERENCES positions(id),
    CONSTRAINT production_logs_sub_position_id_fkey FOREIGN KEY (sub_position_id)
        REFERENCES sub_positions(id),
    CONSTRAINT production_logs_shift_id_fkey FOREIGN KEY (shift_id)
        REFERENCES shifts(id),
    CONSTRAINT production_logs_supplier_id_fkey FOREIGN KEY (supplier_id)
        REFERENCES suppliers(id),
    CONSTRAINT production_logs_item_id_fkey FOREIGN KEY (item_id)
        REFERENCES items(id),
    CONSTRAINT production_logs_approved_coordinator_by_fkey FOREIGN KEY (approved_coordinator_by)
        REFERENCES workers(id),
    CONSTRAINT production_logs_approved_spv_by_fkey FOREIGN KEY (approved_spv_by)
        REFERENCES workers(id)
);

ALTER SEQUENCE production_logs_id_seq OWNED BY production_logs.id;

-- ----------------------------------------------------------------------------
-- Table: production_log_problem_comments
-- Description: Relasi many-to-many antara production_logs dan problem_comments
-- ----------------------------------------------------------------------------
CREATE TABLE production_log_problem_comments (
    id INTEGER NOT NULL DEFAULT nextval('production_log_problem_comments_id_seq'::regclass),
    production_log_id BIGINT NOT NULL,
    problem_comment_id INTEGER NOT NULL,
    CONSTRAINT production_log_problem_comments_pkey PRIMARY KEY (id),
    CONSTRAINT plpc_unique UNIQUE (production_log_id, problem_comment_id),
    CONSTRAINT production_log_problem_comments_production_log_id_fkey FOREIGN KEY (production_log_id)
        REFERENCES production_logs(id) ON DELETE CASCADE,
    CONSTRAINT production_log_problem_comments_problem_comment_id_fkey FOREIGN KEY (problem_comment_id)
        REFERENCES problem_comments(id) ON DELETE RESTRICT
);

ALTER SEQUENCE production_log_problem_comments_id_seq OWNED BY production_log_problem_comments.id;

-- ============================================================================
-- CREATE INDEXES (Optional - for performance optimization)
-- ============================================================================

-- Indexes for foreign keys (if needed for performance)
-- CREATE INDEX idx_production_logs_worker_id ON production_logs(worker_id);
-- CREATE INDEX idx_production_logs_position_id ON production_logs(position_id);
-- CREATE INDEX idx_production_logs_shift_id ON production_logs(shift_id);
-- CREATE INDEX idx_production_logs_item_id ON production_logs(item_id);
-- CREATE INDEX idx_production_logs_created_at ON production_logs(created_at);
-- CREATE INDEX idx_workers_department_id ON workers(department_id);
-- CREATE INDEX idx_workers_position_id ON workers(position_id);
-- CREATE INDEX idx_departments_division_id ON departments(division_id);
-- CREATE INDEX idx_sub_positions_position_id ON sub_positions(position_id);

-- ============================================================================
-- COMMENTS ON TABLES AND COLUMNS
-- ============================================================================

COMMENT ON TABLE divisions IS 'Divisi dalam organisasi (e.g., Kawat, IT)';
COMMENT ON TABLE departments IS 'Departemen dalam divisi (e.g., Operator, Koordinator, Supervisor)';
COMMENT ON TABLE positions IS 'Posisi pekerjaan (e.g., PER, RAM, TEMBAK, POCKET, ASSEMBLY, FRAME, SUPPLY)';
COMMENT ON TABLE sub_positions IS 'Sub posisi atau mesin dalam posisi (e.g., FC60, SX80, MEJA-1)';
COMMENT ON TABLE workers IS 'Pekerja/operator dalam sistem';
COMMENT ON TABLE shifts IS 'Shift kerja (e.g., Shift 1, Shift 2, Shift 3)';
COMMENT ON TABLE suppliers IS 'Supplier material (e.g., Intiroda, Mega, Kingdom)';
COMMENT ON TABLE items IS 'Item produk yang diproduksi';
COMMENT ON TABLE problem_comments IS 'Komentar atau jenis kendala produksi';
COMMENT ON TABLE production_logs IS 'Log produksi harian';
COMMENT ON TABLE production_log_problem_comments IS 'Relasi many-to-many antara production_logs dan problem_comments';

COMMENT ON COLUMN workers.password IS 'Password ter-hash untuk autentikasi worker';
COMMENT ON COLUMN production_logs.qty_output IS 'Jumlah output produksi';
COMMENT ON COLUMN production_logs.qty_reject IS 'Jumlah reject produksi';
COMMENT ON COLUMN production_logs.problem_duration_minutes IS 'Durasi kendala produksi dalam menit';
COMMENT ON COLUMN production_logs.approved_coordinator IS 'Status approval oleh koordinator';
COMMENT ON COLUMN production_logs.approved_spv IS 'Status approval oleh supervisor';
COMMENT ON COLUMN positions.unit IS 'Unit pengukuran: pcs (pieces) atau lmbr (lembar)';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

