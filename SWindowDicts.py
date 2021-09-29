# pylint: disable-msg=E0611
from PyQt5.QtWidgets import QDialog
from ui.SubWindowDicts import Ui_Dictionaries


class SubWindowDicts(QDialog):
    def __init__(self, conn, data):
        super().__init__()
        self.ui = Ui_Dictionaries()
        self.ui.setupUi(self)

        self.conn = conn
        self.data = data

        sql = """DECLARE @cols AS NVARCHAR(MAX),
    @query  AS NVARCHAR(MAX)

select @cols = STUFF((SELECT ',' + QUOTENAME(gds.Name) 
                    from Games g
						left join dbo.GamesDictionarySeries gds on g.Series_id = gds.Id
					group by gds.Name
                    --order by id
            FOR XML PATH(''), TYPE
            ).value('.', 'NVARCHAR(MAX)') 
        ,1,1,'')


set @query = N'SELECT ' + @cols + N' from 
             (select gdc.Name, count(g.id) as XXX
				from dbo.Games g
				left join dbo.GamesDictionaryCategory gdc on g.Category_id = gdc.Id
				group by gdc.Name
            ) x
            pivot 
            (
                max(XXX)
                for x.Name in (' + @cols + N')
            ) p '

exec sp_executesql @query;"""


        self.model = self.conn.sql_refresh(sql, None)
        self.ui.tableView.setModel(self.model)


    def edit_dict_value(self):
        pass

    def refresh(self):
        pass

    def switch_rows_and_columns(self):
        pass

    def details(self):
        pass


# TODO - poprawić układ okienka, jest jakiś taki do dupy