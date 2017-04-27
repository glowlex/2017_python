(function(){

  class Calendar{
    constructor(year=new Date().getFullYear(), month=new Date().getMonth(), day=new Date().getDate()){
      this.date = new Date(year, month, day);
      this.SHORT_DAY_NAMES = new Array(
        'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб');

      this.MONTH_NAMES = new Array(
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
        'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
      );
    }
    init(){
      $("#month_next").click(function(){
        this.date.setMonth(this.date.getMonth()+1);
      });
    }

  }


  var i = new Date(2017, 0, 30);
  var maxDays = 33 - new Date(2017, 1, 33).getDate();
  debugger;
  c = new Calendar();

})();
