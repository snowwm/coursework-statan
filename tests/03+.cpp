// !test sql_injection
#include <iostream>
using namespace std;

int main(){
  QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL","mydb");
  db.setHostName("bigblue");
  db.setDatabaseName("flightdb");
  db.setUserName("acarlson");
  db.setPassworld("1uTbSbAs");
  bool ok = db.open();
  QSqlQuery query;
  scanf("%s",login);
  return 0;
}