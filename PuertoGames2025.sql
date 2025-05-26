-- Crear la base de datos
CREATE DATABASE PuertoGames2025;
GO

-- Usar la base de datos
USE PuertoGames2025;
GO

-- Tabla Plataformas
CREATE TABLE Plataformas (
    id_plataforma INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Insertar plataformas (sin duplicados)
INSERT INTO Plataformas (nombre) VALUES 
('PlayStation 5'), 
('PlayStation 4'), 
('Nintendo Switch'), 
('Xbox'), 
('Steam Deck'), 
('Ubisoft Connect');
GO

-- Tabla Videojuegos
CREATE TABLE Videojuegos (
    id_videojuego INT PRIMARY KEY IDENTITY(1,1),
    titulo VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    id_plataforma INT NOT NULL,
    fecha_agregado DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_plataforma) REFERENCES Plataformas(id_plataforma)
);

-- Insertar videojuegos (eliminando duplicados)
INSERT INTO Videojuegos (titulo, precio, stock, id_plataforma) VALUES
-- PlayStation PS5
('The Last of Us Part II', 40000.00, 15, 1),
('God of War Ragnar�k', 20447.02, 8, 1),
('Astro Bot', 63990.00, 5, 1),
('VALKYRIE ELYSIUM', 40000.00, 8, 1),
('Spider-Man Miles Morales', 50500.00, 15, 1),
('Rollerdrome', 15500.00, 20, 1),
('Inscryption', 4500.00, 5, 1),

-- PlayStation PS4
('The Tomorrow Children: Phoenix Edition', 7500.00, 7, 2),
('Stray', 14900.00, 12, 2),
('Ghostwire: Tokyo', 5500.00, 7, 2),
('VALKYRIE ELYSIUM PS4', 35000.00, 8, 2),
('The Last of Us Part I', 40000.00, 15, 2),

-- Nintendo Switch
('The Legend of Zelda: Breath of the Wild', 39990.00, 20, 3),
('Mario Kart 8 Deluxe', 49990.00, 18, 3),
('Animal Crossing: New Horizons', 20700.00, 25, 3),
('Hyrule Warriors: la Era del Cataclismo', 20000.00, 10, 3),
('ARK Switch', 10000.00, 20, 3),
('Super Mario 3D', 49990.00, 19, 3),
('Nintendo Switch Sports', 19990.00, 15, 3),
('Splatoon 3', 19990.00, 12, 3),
('Darksiders III', 29990.00, 17, 3),
('Super Mario Bros. Wonder', 59990.00, 25, 3),

-- Xbox
('Grand Theft Auto V', 11000.00, 30, 4),
('Call of Duty: Modern Warfare II', 60000.00, 9, 4),
('Minecraft', 30000.00, 40, 4),
('Subnautica', 6000.00, 9, 4),
('ARK Xbox', 5000.00, 10, 4),
('Crime Scene Cleaner', 16000.00, 12, 4),
('EA Sports Madden NFL 25', 50000.00, 18, 4),
('Path of Exile 2', 20000.00, 9, 4),
('Rust', 6000.00, 18, 4),
('The Elder Scrolls IV: Oblivion Remastered', 60000.00, 9, 4),

-- Steam Deck
('Baldurs Gate 3', 20000.00, 12, 5),
('The Witcher 3: Wild Hunt', 15000.00, 15, 5),
('DOOM (2016)', 4000.00, 8, 5),
('Schedule I', 4000.00, 7, 5),
('Monster Hunter Wilds', 4000.00, 8, 5),
('R.E.P.O', 4000.00, 7, 5),
('Alien: Isolation', 4000.00, 12, 5),
('Slime Rancher', 4000.00, 14, 5),
('Sons of the Forest', 4000.00, 7, 5),
('Kingdom Come: Deliverance', 4000.00, 19, 5),

-- Ubisoft Connect
('Assassins Creed Shadows', 70000.00, 6, 6),
('Far Cry 6', 69000.00, 7, 6),
('Rainbow Six Siege', 49990.00, 14, 6),
('Watch Dogs: Legion', 49990.00, 17, 6),
('Prince of Persia The Lost Crown', 49990.00, 17, 6),
('Skull & Bones', 49990.00, 17, 6),
('Assassins Creed Mirage', 49990.00, 10, 6),
('Assassins Creed Valhalla', 59990.00, 11, 6),
('Avatar: Frontiers of Pandora', 49990.00, 17, 6);
GO

-- Vista para consultas mas faciles
CREATE VIEW VistaVideojuegos AS
SELECT 
    v.id_videojuego,
    v.titulo,
    v.precio,
    v.stock,
    p.nombre as plataforma,
    v.fecha_agregado
FROM Videojuegos v
INNER JOIN Plataformas p ON v.id_plataforma = p.id_plataforma;
GO

-- Consulta de prueba
SELECT * FROM VistaVideojuegos ORDER BY titulo;