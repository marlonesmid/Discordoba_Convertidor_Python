SET NOCOUNT ON;
BEGIN TRANSACTION;

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12580', 'Marcela Giraldo', '43741169', 'Logout', '2026-02-12 15:02:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12580', 'Marcela Giraldo', '43741169', 'Logout', '2026-02-12 15:02:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12582', 'Laura Portillo', '1143165625', 'Ready', '2026-03-11 08:07:33', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12582', 'Laura Portillo', '1143165625', 'Ready', '2026-03-11 08:07:33', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12585', 'Lina Mayorga', '1022982409', 'Logout', '2026-03-10 08:03:45', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12585', 'Lina Mayorga', '1022982409', 'Logout', '2026-03-10 08:03:45', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12588', 'Brenda Restrepo', '1031121568', 'Ready', '2026-03-11 08:21:15', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12588', 'Brenda Restrepo', '1031121568', 'Ready', '2026-03-11 08:21:15', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12592', 'Madela Gutiérrez', '1143250489', 'AUX', '2026-03-11 10:51:13', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12592', 'Madela Gutiérrez', '1143250489', 'AUX', '2026-03-11 10:51:13', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12593', 'Paula Gonzalez', '43877181', 'AUX', '2026-03-11 12:27:29', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12593', 'Paula Gonzalez', '43877181', 'AUX', '2026-03-11 12:27:29', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12597', 'Luisa Gómez', '1216719616', 'Logout', '2026-03-11 12:33:26', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12597', 'Luisa Gómez', '1216719616', 'Logout', '2026-03-11 12:33:26', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12601', 'Joanna Molina', '1047336655', 'Ready', '2026-03-11 08:19:13', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12601', 'Joanna Molina', '1047336655', 'Ready', '2026-03-11 08:19:13', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12610', 'Jimena Montealegre', '1144172466', 'Logout', '2026-03-10 08:31:23', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12610', 'Jimena Montealegre', '1144172466', 'Logout', '2026-03-10 08:31:23', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12615', 'Anderson Pulido', '1010170695', 'Logout', '2026-02-25 10:07:49', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12615', 'Anderson Pulido', '1010170695', 'Logout', '2026-02-25 10:07:49', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12618', 'Jacqueline Murcia', '52861950', 'Ready', '2026-03-11 08:55:24', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12618', 'Jacqueline Murcia', '52861950', 'Ready', '2026-03-11 08:55:24', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12620', 'Tatiana Villamil', '1013122250', 'Ready', '2026-03-11 12:42:04', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12620', 'Tatiana Villamil', '1013122250', 'Ready', '2026-03-11 12:42:04', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12626', 'Arelis Sanchez', NULL, 'Logout', '2026-02-05 17:57:47', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12626', 'Arelis Sanchez', NULL, 'Logout', '2026-02-05 17:57:47', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12672', 'Prueba', '1024504557', 'Logout', '2025-12-31 10:50:50', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12672', 'Prueba', '1024504557', 'Logout', '2025-12-31 10:50:50', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12797', 'Laura Berrios', '1020448478', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12797', 'Laura Berrios', '1020448478', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12804', 'Camila Ramirez', '1010137342', 'Ready', '2026-03-11 10:29:59', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12804', 'Camila Ramirez', '1010137342', 'Ready', '2026-03-11 10:29:59', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12811', 'Myriam Rodriguez', '37394269', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12811', 'Myriam Rodriguez', '37394269', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12815', 'Yesica Suarez', '1066179565', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12815', 'Yesica Suarez', '1066179565', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12816', 'Beatriz Usma', '43748999', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12816', 'Beatriz Usma', '43748999', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12817', 'Paola Ramirez', '38888128', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12817', 'Paola Ramirez', '38888128', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12818', 'Lyda Galan', '46375186', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12818', 'Lyda Galan', '46375186', 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12829', 'Estefania Ramos', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12829', 'Estefania Ramos', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12833', 'Alexandra Chavarro', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12833', 'Alexandra Chavarro', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12839', 'Ana Carola Silva', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12839', 'Ana Carola Silva', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12855', 'Carmenza Barandica', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12855', 'Carmenza Barandica', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12878', 'Stefania Sanchez', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12878', 'Stefania Sanchez', NULL, 'Logout', '2026-02-25 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12895', 'Adriana Monsalve', NULL, 'Logout', '2026-02-12 00:00:00', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12895', 'Adriana Monsalve', NULL, 'Logout', '2026-02-12 00:00:00', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12906', 'Sandra Rodriguez', '52055354', 'Ready', '2026-03-11 11:04:18', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12906', 'Sandra Rodriguez', '52055354', 'Ready', '2026-03-11 11:04:18', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12907', 'Valentina Mora', '1000328210', 'AUX', '2026-03-11 10:30:22', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12907', 'Valentina Mora', '1000328210', 'AUX', '2026-03-11 10:30:22', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12911', 'Andrea Hernández', '1016054809', 'Logout', '2026-03-06 08:20:08', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12911', 'Andrea Hernández', '1016054809', 'Logout', '2026-03-06 08:20:08', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12915', 'Laura Castellanos', '1014738239', 'AUX', '2026-03-11 08:06:17', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12915', 'Laura Castellanos', '1014738239', 'AUX', '2026-03-11 08:06:17', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12919', 'Lidiana Londoño', '43727745', 'Ready', '2026-03-11 08:21:46', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12919', 'Lidiana Londoño', '43727745', 'Ready', '2026-03-11 08:21:46', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12924', 'Derly Baracaldo', '1018482181', 'AUX', '2026-03-11 11:08:42', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12924', 'Derly Baracaldo', '1018482181', 'AUX', '2026-03-11 11:08:42', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12934', 'Tatiana Muñoz', '1107086149', 'Ready', '2026-03-11 12:36:54', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12934', 'Tatiana Muñoz', '1107086149', 'Ready', '2026-03-11 12:36:54', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12978', 'Cristian Patiño', '1006238983', 'Logout', '2026-02-24 13:56:16', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12978', 'Cristian Patiño', '1006238983', 'Logout', '2026-02-24 13:56:16', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12991', 'Marilu', '86000615', 'Logout', '2026-02-04 15:26:35', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12991', 'Marilu', '86000615', 'Logout', '2026-02-04 15:26:35', NULL, 'yes', '2026-03-11 13:08:43');

MERGE INTO QUIRAMA.dbo.Integracion_Wolkvox_agentes AS target
USING (SELECT '12996', 'Jazmín Hernández', '52427278', 'Ready', '2026-03-11 12:33:40', NULL, 'yes', '2026-03-11 13:08:43') AS source (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at)
ON target.agent_id = source.agent_id
WHEN MATCHED THEN
    UPDATE SET target.agent_name = source.agent_name, target.agent_dni = source.agent_dni, target.agent_status = source.agent_status, target.last_use = source.last_use, target.agent_sso = source.agent_sso, target.enabled = source.enabled, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (agent_id, agent_name, agent_dni, agent_status, last_use, agent_sso, enabled, updated_at) VALUES ('12996', 'Jazmín Hernández', '52427278', 'Ready', '2026-03-11 12:33:40', NULL, 'yes', '2026-03-11 13:08:43');

COMMIT TRANSACTION;
