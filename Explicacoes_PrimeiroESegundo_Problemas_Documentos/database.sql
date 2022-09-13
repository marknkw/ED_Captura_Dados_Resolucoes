CREATE TABLE [Sanaeantes] (
  [idAssunto] int,
  [idCategoria] int,
  [idEmpresa] int,
  [idResolucao] int,
  [idVendaEmprego] int,
  [idApresentacao] int,
  [Description] nvarchar(255),
  PRIMARY KEY ([idAssunto], [idCategoria], [idEmpresa], [idResolucao], [idVendaEmprego], [idApresentacao])
)
GO

CREATE TABLE [Assunto] (
  [id] int PRIMARY KEY,
  [Description] nvarchar(255)
)
GO

CREATE TABLE [Categoria] (
  [id] int PRIMARY KEY,
  [Description] nvarchar(255)
)
GO

CREATE TABLE [Empresa] (
  [id] int PRIMARY KEY,
  [Empresa] nvarchar(255),
  [Marca] nvarchar(255),
  [Processo] nvarchar(255),
  [Registro] nvarchar(255),
  [Autorizacao] nvarchar(255)
)
GO

CREATE TABLE [Resolucao] (
  [id] int PRIMARY KEY,
  [Description] nvarchar(255)
)
GO

CREATE TABLE [VendaEmprego] (
  [id] int PRIMARY KEY,
  [Description] nvarchar(255)
)
GO

CREATE TABLE [Apresentacao] (
  [id] int PRIMARY KEY,
  [Description] nvarchar(255)
)
GO

ALTER TABLE [Sanaeantes] ADD FOREIGN KEY ([idCategoria]) REFERENCES [Categoria] ([id])
GO

ALTER TABLE [Sanaeantes] ADD FOREIGN KEY ([idAssunto]) REFERENCES [Assunto] ([id])
GO

ALTER TABLE [Empresa] ADD FOREIGN KEY ([id]) REFERENCES [Sanaeantes] ([idEmpresa])
GO

ALTER TABLE [Resolucao] ADD FOREIGN KEY ([id]) REFERENCES [Sanaeantes] ([idResolucao])
GO

ALTER TABLE [VendaEmprego] ADD FOREIGN KEY ([id]) REFERENCES [Sanaeantes] ([idVendaEmprego])
GO

ALTER TABLE [Apresentacao] ADD FOREIGN KEY ([id]) REFERENCES [Sanaeantes] ([idApresentacao])
GO
