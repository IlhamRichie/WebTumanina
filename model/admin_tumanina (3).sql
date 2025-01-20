-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 20, 2025 at 07:49 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `admin_tumanina`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content` text COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `content`, `image`, `created_at`) VALUES
(27, 'Keindahan Akhlak Rasulullah SAW', 'Rasulullah SAW adalah teladan utama bagi umat manusia dalam segala aspek kehidupan. Salah satu aspek yang paling menonjol dari kepribadian beliau adalah akhlaknya yang mulia. Bahkan Allah SWT sendiri memuji akhlak beliau dalam Al-Qur’an, “Dan sesungguhnya engkau benar-benar berbudi pekerti yang agung” (QS. Al-Qalam: 4).\nAkhlak Rasulullah mencakup berbagai dimensi, mulai dari kejujuran, kesabaran, kasih sayang, hingga keadilan. Sebagai contoh, beliau dikenal sebagai “Al-Amin” atau yang dapat dipercaya jauh sebelum diangkat menjadi nabi. Sikap jujur beliau membuat masyarakat Mekkah merasa nyaman menitipkan harta kepada beliau, bahkan dari kalangan yang menentangnya.\nSikap kasih sayang Rasulullah SAW tidak hanya terbatas pada keluarga dan sahabat, tetapi juga meliputi anak-anak, orang tua, dan bahkan binatang. Dalam sebuah riwayat, Rasulullah menegur seorang sahabat yang mengganggu seekor burung dengan mengambil anak-anaknya. Beliau berkata, “Siapa yang membuat burung ini merasa terganggu dengan mengambil anak-anaknya? Kembalikanlah anak-anak itu kepadanya.”\nSelain itu, Rasulullah SAW adalah sosok yang sangat adil. Ketika seorang wanita dari Bani Makhzum mencuri dan masyarakat mencoba melobi agar hukum tidak diberlakukan, Rasulullah bersabda, “Jika Fatimah binti Muhammad mencuri, maka aku sendiri yang akan memotong tangannya.” Hal ini menunjukkan bahwa beliau tidak membedakan orang dalam menegakkan hukum Allah.\nAkhlak mulia Rasulullah adalah pelajaran abadi bagi umat manusia. Sebagai umatnya, kita diharuskan meneladani beliau dalam kehidupan sehari-hari, baik dalam hubungan dengan Allah, sesama manusia, maupun alam.\n', 'Mengapa-Islam-Agama-yang-Benar.png', '2025-01-12 00:31:00'),
(28, 'Pentingnya Ilmu dalam Islam', 'Islam adalah agama yang sangat menghargai ilmu pengetahuan. Ayat pertama yang diturunkan kepada Rasulullah SAW berbunyi, “Bacalah dengan (menyebut) nama Tuhanmu yang menciptakan” (QS. Al- ‘Alaq: 1). Ayat ini menunjukkan bahwa membaca dan mencari ilmu adalah kewajiban utama seorang muslim.\nDalam sebuah hadis, Rasulullah SAW bersabda, “Menuntut ilmu adalah kewajiban bagi setiap muslim.” (HR. Ibnu Majah). Hadis ini menegaskan bahwa kewajiban menuntut ilmu tidak terbatas pada laki-laki, tetapi juga berlaku untuk perempuan. Ilmu dianggap sebagai jalan untuk memahami kebesaran Allah dan menjalani kehidupan yang lebih baik.\nPara ulama di masa keemasan Islam seperti Al-Khwarizmi, Ibnu Sina, dan Al-Farabi menunjukkan bagaimana Islam mendorong umatnya untuk memajukan ilmu pengetahuan. Mereka tidak hanya menguasai ilmu agama tetapi juga sains, matematika, kedokteran, dan filsafat. Banyak penemuan yang mereka hasilkan menjadi dasar dari perkembangan ilmu pengetahuan modern.\nIslam juga mengajarkan bahwa ilmu tidak hanya untuk kepentingan pribadi, tetapi harus bermanfaat bagi masyarakat. Rasulullah SAW bersabda, “Sebaik-baik manusia adalah yang paling bermanfaat bagi orang lain.” Ilmu yang bermanfaat adalah amal jariyah yang pahalanya akan terus mengalir meskipun seseorang telah meninggal dunia.\nDengan menuntut ilmu, umat Islam tidak hanya akan meningkatkan kualitas hidupnya, tetapi juga mampu memberikan kontribusi positif bagi dunia. Oleh karena itu, mari kita jadikan ilmu sebagai bagian penting dari hidup kita.\n', 'foto-orang-bersujud-60b909618ede.png', '2025-01-12 00:33:00'),
(29, 'Makna Ibadah dalam Kehidupan Muslim', 'Ibadah adalah inti dari kehidupan seorang muslim. Dalam Islam, ibadah tidak hanya terbatas pada ritual seperti shalat, puasa, zakat, dan haji, tetapi juga mencakup segala aktivitas yang dilakukan dengan niat ikhlas karena Allah SWT. Dalam Al-Qur’an, Allah berfirman, “Dan Aku tidak menciptakan jin dan manusia melainkan supaya mereka beribadah kepada-Ku” (QS. Adz-Dzariyat: 56).\nShalat, sebagai tiang agama, adalah bentuk ibadah utama yang mendekatkan seorang hamba kepada Allah. Rasulullah SAW bersabda, “Shalat adalah cahaya.” Shalat yang dilakukan dengan khusyuk dan benar akan membentuk karakter yang baik dan mencegah perbuatan keji dan mungkar.\nSelain shalat, ibadah puasa melatih seorang muslim untuk memiliki pengendalian diri dan rasa empati terhadap sesama, khususnya mereka yang kurang mampu. Zakat dan sedekah adalah bentuk ibadah sosial yang membantu pemerataan kekayaan dan mengurangi kemiskinan.\nNamun, ibadah dalam Islam tidak hanya bersifat ritual. Bekerja mencari nafkah untuk keluarga, menuntut ilmu, bahkan tersenyum kepada orang lain juga termasuk ibadah jika dilakukan dengan niat yang benar. Rasulullah SAW bersabda, “Senyummu kepada saudaramu adalah sedekah.”\nMakna ibadah dalam Islam sangat luas dan mencakup seluruh aspek kehidupan. Dengan memahami konsep ini, seorang muslim dapat menjadikan setiap aktivitasnya sebagai jalan untuk mendekatkan diri kepada Allah SWT.\n', 'makna-ibadah.png', '2025-01-12 00:34:00'),
(30, 'Konsep Keadilan dalam Islam', 'Keadilan adalah salah satu nilai fundamental dalam ajaran Islam. Allah SWT berfirman dalam Al-Qur’an, “Sesungguhnya Allah menyuruh (kamu) berlaku adil dan berbuat kebajikan” (QS. An-Nahl: 90). Ayat ini menunjukkan bahwa keadilan adalah perintah langsung dari Allah yang harus ditegakkan dalam kehidupan pribadi maupun sosial.\nKeadilan dalam Islam tidak hanya berarti memberikan hak kepada yang berhak, tetapi juga melibatkan sikap tidak berat sebelah, jujur, dan bertanggung jawab. Rasulullah SAW adalah contoh nyata bagaimana keadilan ditegakkan. Dalam sebuah riwayat, beliau menolak memberikan perlakuan istimewa kepada seorang wanita bangsawan yang mencuri. Beliau menegaskan bahwa hukum Allah berlaku untuk semua orang tanpa memandang status sosial.\nDalam Islam, keadilan juga mencakup hubungan antara manusia dengan alam. Manusia diberi amanah sebagai khalifah di bumi untuk menjaga keseimbangan ekosistem. Eksploitasi berlebihan terhadap sumber daya alam dianggap melanggar prinsip keadilan karena akan merugikan generasi mendatang.\nKeadilan ekonomi juga ditekankan dalam Islam. Zakat, sedekah, dan larangan riba adalah beberapa contoh bagaimana Islam berupaya menciptakan sistem ekonomi yang adil. Sistem ini bertujuan untuk mengurangi kesenjangan antara si kaya dan si miskin.\nDengan menegakkan keadilan, umat Islam dapat menciptakan masyarakat yang harmonis dan penuh berkah. Oleh karena itu, mari kita jadikan prinsip keadilan sebagai pedoman dalam setiap aspek kehidupan kita.\n \n', '213214.png', '2025-01-12 00:35:00');

-- --------------------------------------------------------

--
-- Table structure for table `discussions`
--

CREATE TABLE `discussions` (
  `id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `user_apk_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `discussions`
--

INSERT INTO `discussions` (`id`, `title`, `content`, `user_id`, `user_apk_id`, `created_at`, `updated_at`) VALUES
(7, 'gsgsgs', 'shshsh', 30, 2, '2025-01-20 13:30:45', '2025-01-20 13:30:45'),
(8, 'jajaja', 'aakakka', 30, 1, '2025-01-20 13:41:03', '2025-01-20 13:41:03'),
(9, 'aajaj', 'ajjaja', 34, 2, '2025-01-20 13:51:45', '2025-01-20 13:51:45'),
(11, 'fffff', 'fff', 34, 2, '2025-01-20 14:44:59', '2025-01-20 14:44:59');

-- --------------------------------------------------------

--
-- Table structure for table `discussion_comments`
--

CREATE TABLE `discussion_comments` (
  `id` int NOT NULL,
  `discussion_id` int NOT NULL,
  `comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_apk_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `discussion_comments`
--

INSERT INTO `discussion_comments` (`id`, `discussion_id`, `comment`, `user_apk_id`, `created_at`, `updated_at`) VALUES
(1, 8, 'hahahaha', 1, '2025-01-20 13:47:35', '2025-01-20 13:47:35'),
(2, 7, 'hhahaha', 1, '2025-01-20 13:49:04', '2025-01-20 13:49:04'),
(3, 8, 'hahaha', 1, '2025-01-20 13:50:38', '2025-01-20 13:50:38'),
(4, 9, 'wkwkkw', 1, '2025-01-20 14:03:54', '2025-01-20 14:03:54'),
(5, 9, 'halo', 1, '2025-01-20 14:09:18', '2025-01-20 14:09:18'),
(7, 7, 'tailaso', 1, '2025-01-20 14:32:51', '2025-01-20 14:32:51'),
(8, 7, 'astagfirullah', 1, '2025-01-20 14:33:02', '2025-01-20 14:33:02');

-- --------------------------------------------------------

--
-- Table structure for table `hasil_model`
--

CREATE TABLE `hasil_model` (
  `id_hasil_model` int NOT NULL,
  `nama` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `tanggal` date NOT NULL,
  `review` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `label` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `id_review` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hasil_model`
--

INSERT INTO `hasil_model` (`id_hasil_model`, `nama`, `tanggal`, `review`, `label`, `id_review`) VALUES
(23, 'hai', '2024-12-23', 'aplikasinya keren banget', 'Positif', 22),
(26, 'satrio', '2025-01-08', 'bagus aplikasinya', 'Positif', 25),
(27, 'satrio', '2025-01-08', 'aplikasinya bagus bener dah', 'Positif', 26),
(28, 'ilham', '2025-01-08', 'bagus baget aplikasinya', 'Positif', 27),
(29, 'ilham', '2025-01-08', 'bagus baget aplikasinya', 'Positif', 28),
(30, 'satrio', '2025-01-09', 'aplikasinya sangat bermanfaat', 'Positif', 29);

-- --------------------------------------------------------

--
-- Table structure for table `input_review`
--

CREATE TABLE `input_review` (
  `id_review` int NOT NULL,
  `nama` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `tanggal` date NOT NULL,
  `review` varchar(1000) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `input_review`
--

INSERT INTO `input_review` (`id_review`, `nama`, `tanggal`, `review`) VALUES
(22, 'hai', '2024-12-23', 'aplikasinya keren banget'),
(25, 'satrio', '2025-01-08', 'bagus aplikasinya'),
(26, 'satrio', '2025-01-08', 'aplikasinya bagus bener dah'),
(27, 'ilham', '2025-01-08', 'bagus baget aplikasinya'),
(28, 'ilham', '2025-01-08', 'bagus baget aplikasinya'),
(29, 'satrio', '2025-01-09', 'aplikasinya sangat bermanfaat');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('super_admin','admin') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(30, 'superadmin', 'scrypt:32768:8:1$IxObJXNW7hgVFqCI$400f9c1a08f58528dc5a2dabe55a846cb5626843115bdb6f655caeb1ad2ae4e37b9bbdc7f9c1a97c46279d820d0464d95bfd4d0603bceff66706099918289031', 'super_admin'),
(34, 'adminbiasa', 'scrypt:32768:8:1$DHMEDbauAXmO00It$33440acb3f26e3a1cf5d9ca1709068802966e2ed4e23e56a53513d62aa0cb179a6afb7e0983f4bc040319451f379dcc4d429e8454bf806fdd17d2d0646ddf0df', 'admin'),
(35, 'admin2', 'scrypt:32768:8:1$9t3JFPtHzfxUAVEn$22064dc23c5f0e9c9ae2addbb090ac110b7045a0f12e98c6c7c6529fe790f90e7fed1989c5744664b678a2083e25f314ee59f8a56e93dca4417dc013d4f3a5a9', 'super_admin');

-- --------------------------------------------------------

--
-- Table structure for table `users_apk`
--

CREATE TABLE `users_apk` (
  `id` int NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users_apk`
--

INSERT INTO `users_apk` (`id`, `username`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'john_doe', 'john.doe@example.com', '$2b$12$abcdefgh1234567890ABCDEFGHIJ1234567890abcdefgh1234', '2025-01-20 08:57:15', '2025-01-20 08:57:15'),
(2, 'jane_smith', 'jane.smith@example.com', '$2b$12$JKLMNOPQ9876543210qrstuvwxyz0987654321JKLMNOPQ9876', '2025-01-20 08:57:15', '2025-01-20 08:57:15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `discussions`
--
ALTER TABLE `discussions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `user_apk_id` (`user_apk_id`);

--
-- Indexes for table `discussion_comments`
--
ALTER TABLE `discussion_comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `discussion_id` (`discussion_id`),
  ADD KEY `user_apk_id` (`user_apk_id`);

--
-- Indexes for table `hasil_model`
--
ALTER TABLE `hasil_model`
  ADD PRIMARY KEY (`id_hasil_model`);

--
-- Indexes for table `input_review`
--
ALTER TABLE `input_review`
  ADD PRIMARY KEY (`id_review`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `users_apk`
--
ALTER TABLE `users_apk`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `discussions`
--
ALTER TABLE `discussions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `discussion_comments`
--
ALTER TABLE `discussion_comments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `hasil_model`
--
ALTER TABLE `hasil_model`
  MODIFY `id_hasil_model` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `input_review`
--
ALTER TABLE `input_review`
  MODIFY `id_review` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `users_apk`
--
ALTER TABLE `users_apk`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `discussions`
--
ALTER TABLE `discussions`
  ADD CONSTRAINT `discussions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `discussions_ibfk_2` FOREIGN KEY (`user_apk_id`) REFERENCES `users_apk` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `discussion_comments`
--
ALTER TABLE `discussion_comments`
  ADD CONSTRAINT `discussion_comments_ibfk_1` FOREIGN KEY (`discussion_id`) REFERENCES `discussions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `discussion_comments_ibfk_2` FOREIGN KEY (`user_apk_id`) REFERENCES `users_apk` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
