data "external_schema" "sqlalchemy" {
  program = [
    "poetry",
    "run",
    "python3",
    "-m",
    "yalchat_server",
    "print_ddl"
  ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = "docker://postgres/15/dev?&sslmode=disable"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
