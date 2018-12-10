CREATE TABLE public.perfil_produtor (
  id_produtor serial NOT NULL,
  nome_loja varchar(30) NOT NULL,
  cnpj varchar(18) NULL,
  descricao_loja varchar(300) NULL,
  contato_comercial varchar(16) NOT NULL,
  endereco_comercial varchar(50) NULL,
  foto_loja varchar(400) DEFAULT NULL,
  UNIQUE (cnpj),
  CONSTRAINT perfil_produtor_pkey PRIMARY KEY (id_produtor)
);

CREATE TABLE public.perfil (
  id serial NOT NULL,
  nome varchar(10) NOT NULL,
  sobrenome varchar(15) NOT NULL,
  contato varchar(16) NOT NULL,
  cidade varchar(30) NOT NULL,
  bairro varchar(50) NOT NULL,
  endereco varchar(50) NOT NULL,
  cpf varchar(14) NOT NULL,
  email varchar(30) NOT NULL,
  senha varchar(15) NOT NULL,
  id_produtor int NULL,
  CONSTRAINT perfil_cpf_key UNIQUE (cpf),
  CONSTRAINT perfil_email_key UNIQUE (email),
  CONSTRAINT perfil_id_produtor_key UNIQUE (id_produtor),
  CONSTRAINT perfil_pkey PRIMARY KEY (id),
  CONSTRAINT perfil_id_produtor_fkey FOREIGN KEY (id_produtor) REFERENCES perfil_produtor(id_produtor) ON DELETE SET NULL
);




CREATE TABLE public.categoria (
  id_categoria serial NOT NULL,
  nome_categoria varchar(30) NOT NULL,
  CONSTRAINT categoria_pkey PRIMARY KEY (id_categoria)
);

CREATE OR REPLACE FUNCTION public.atualiza_timestamp()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.atualizado_em = NOW();
  RETURN NEW;
END;
$function$
;

CREATE TABLE public.produto (
  id_produto serial NOT NULL,
  nome_produto varchar(20) NOT NULL,
  id_categoria int4 NOT NULL,
  subcategoria varchar(30) NULL,
  preco numeric(6,2) NOT NULL,
  estoque numeric(4) NOT NULL,
  foto_produto varchar(300) NOT NULL,
  descricao_produto varchar(300) NOT NULL,
  id_produtor int4 NOT NULL,
  ativo bool NULL DEFAULT true,
  criado_em timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT produto_pkey PRIMARY KEY (id_produto),
  CONSTRAINT categoria_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
  CONSTRAINT produto_id_produtor_fkey FOREIGN KEY (id_produtor) REFERENCES perfil_produtor(id_produtor)
);


--  Trigger pedido

create
    trigger atualiza_timestamp before update
        on
        public.produto for each row execute procedure atualiza_timestamp();


CREATE TABLE public.pedido (
  id_pedido serial NOT NULL,
  id_produto int4 NOT NULL,
  id_comprador int4 NOT NULL,
  id_produtor int4 NOT NULL,
  quantidade numeric(4) NOT NULL,
  valor numeric(6,2) NOT NULL,
  status bpchar(1) NOT NULL DEFAULT 'P'::bpchar,
  criado_em timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT pedido_pkey PRIMARY KEY (id_pedido),
  CONSTRAINT pedido_id_comprador_fkey FOREIGN KEY (id_comprador) REFERENCES perfil(id),
  CONSTRAINT pedido_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
  CONSTRAINT pedido_id_produtor_fkey FOREIGN KEY (id_produtor) REFERENCES perfil_produtor(id_produtor)
);

--  Trigger pedido

create
    trigger atualiza_timestamp before update
        on
        public.pedido for each row execute procedure atualiza_timestamp();








