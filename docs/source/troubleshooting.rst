Troubleshooting
===============

GROUP_CONCAT row limit in Mysql is too low
------------------------------------------

Mysql has fairly low limit for rows that can be merged by the `GROUP_CONCAT`
function. For large result sets, this has to be increased. This can be done by
the following SQL statement, which can be executed in `open_db_connection`.::

    @classmethod
    def open_db_connection(self):
        conn = MySQLdb.connect(....)
        cursor = conn.cursor()

        cursor.execute('SET SESSION group_concat_max_len = 60000000;')
        return conn
