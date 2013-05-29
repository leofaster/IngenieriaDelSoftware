-- Sección de la empresa
insert into EMPRESA values
(12345678,'TVCABLE');


-- Sección de clientes
insert into CLIENTE values
(22714709,'Gustavo El Khoury','Urb. Monte Elena Qta. Santa Teresa');

insert into CLIENTE values
(20978913,'Rebeca Machado','San Antonio, Los Teques');

insert into CLIENTE values
(21205002,'Paul Baptista','Urb. Monte Monte Elena Qta. La Niebla');

insert into CLIENTE values
(21205003,'Victor Sanchez','Urb. Monte Monte Elena Qta. La Niebla');

insert into CLIENTE values
(21205004,'Fabio Castro','Urb. El Placer');

insert into CLIENTE values
(21205005,'Catherine Lollett','Los Guayabitos');

insert into CLIENTE values
(21205006,'Roberto Goncalves','Urb. Monte Elena Qta. Santa Teresa');

insert into CLIENTE values
(21205007,'Marina Salas','Petare');

insert into CLIENTE values
(21205008,'Yohnaikel Mendoze','Las Minas de Baruta');

insert into CLIENTE values
(21205009,'Caren Lengster','La Lagunita');

insert into CLIENTE values
(21205010,'Juan Perez','Maracacuay');

insert into CLIENTE values
(21205011,'Victor de Ponte','Las Mercedes');

insert into CLIENTE values
(21205012,'Lisset Herrera','Charallave');

insert into CLIENTE values
(21205013,'Juan Pobre','Cartanal');

insert into CLIENTE values
(21205014,'Andrea Medina','Quinta Crespo');

insert into CLIENTE values
(21205015,'Karla Vera','Chacao');

insert into CLIENTE values
(21205016,'Victoria Guerra','Cua');

insert into CLIENTE values
(21205017,'Andres Benitez','Catia');

insert into CLIENTE values
(21205018,'Maickel Suarez','Las Minas de Baruta');

insert into CLIENTE values
(21205019,'Pedro Lengster','La Lagunita');


-- Sección de los 
insert into PRODUCTO values
('A001','Decodificador','12345678',22714709);

insert into PRODUCTO values
('A002','Decodificador','12345678',22714709);

insert into PRODUCTO values
('A003','Decodificador','12345678',22714709);

insert into PRODUCTO values
('A004','Decodificador','12345678',22714709);


-- Sección de servicios 
insert into SERVICIO values 
(1001,'Canal Nacional',0,FALSE);

insert into SERVICIO values 
(1002,'Canal de Variedades',0,FALSE);

insert into SERVICIO values 
(1003,'Canal de Deportes',0,FALSE);

insert into SERVICIO values 
(1004,'Canal de Kids',0,FALSE);

insert into SERVICIO values 
(1005,'Canal de Cine',0,FALSE);

insert into SERVICIO values 
(1006,'Canal de Mundos',0,FALSE);

insert into SERVICIO values 
(1007,'Canal de Radio',0,FALSE);

insert into SERVICIO values 
(1008,'TVBrasil',42,TRUE);

insert into SERVICIO values 
(1009,'SPN',30,TRUE);

insert into SERVICIO values 
(1010,'NoticiasMundial',35,TRUE);

insert into SERVICIO values 
(1011,'Película PPV',12,FALSE);

-- Sección de planes
insert into plan values
(3001,'TVCABLE Bronce','...',140,150,'prepago');

insert into plan values
(3002,'TVCABLE Bronce','...',140,150,'postpago');

insert into plan values
(3003,'TVCABLE Plata','...',220,250,'prepago');

insert into plan values
(3004,'TVCABLE Plata','...',220,250,'postpago');


-- Sección de servicios para planes

-- Servicios incluidos para el plan TVCABLE Bronce
insert into incluye values
(3001,1001,0.1,14);

insert into incluye values
(3001,1002,0.23,15);

insert into incluye values
(3001,1003,0.25,4);

insert into incluye values
(3001,1004,0.12,4);

insert into incluye values
(3001,1005,0.9,4);

insert into incluye values
(3001,1006,0.1,9);

insert into incluye values
(3001,1007,0.3,7);

--

insert into incluye values
(3002,1001,NULL,14);

insert into incluye values
(3002,1002,NULL,15);

insert into incluye values
(3002,1003,NULL,4);

insert into incluye values
(3002,1004,NULL,4);

insert into incluye values
(3002,1005,NULL,4);

insert into incluye values
(3002,1006,NULL,9);

insert into incluye values
(3002,1007,NULL,7);


-- Servicios incluidos para el plan TVCABLE Plata
insert into incluye values
(3003,1001,0.14,14);

insert into incluye values
(3003,1002,0.12,28);

insert into incluye values
(3003,1003,0.65,9);

insert into incluye values
(3003,1004,0.7,7);

insert into incluye values
(3003,1005,0.1,10);

insert into incluye values
(3003,1006,0.2,20);

insert into incluye values
(3003,1007,0.4,37);



insert into incluye values
(3004,1001,NULL,14);

insert into incluye values
(3004,1002,NULL,28);

insert into incluye values
(3004,1003,NULL,9);

insert into incluye values
(3004,1004,NULL,7);

insert into incluye values
(3004,1005,NULL,10);

insert into incluye values
(3004,1006,NULL,20);

insert into incluye values
(3004,1007,NULL,37);



-- Afiliaciones
insert into ACTIVA values
('A001',3001,0);

insert into AFILIA values
('A002',3002,'paquete');

insert into AFILIA values
('A003',3004,'paquete');

insert into CONTRATA values
('A004',1008);

insert into CONSUME values
('A001',1001,CURRENT_DATE,5);
