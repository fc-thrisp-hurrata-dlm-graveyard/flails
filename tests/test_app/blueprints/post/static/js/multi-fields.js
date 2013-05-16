$(document).ready(function()
    {//_.templateSettings = {
     //       interpolate : /\{\{(.+?)\}\}/g
     //       };
     $('.input-append.date').datepicker();
     if($('.values-jelement-work').length>0){
        var worktemplate = $("#getWorkTemplate").html();
        var id_of_work = $('.values-jelement-work').find('table').attr('id').slice(0,-2);
        var w_num = $('.values-jelement-work').find('table').attr('id').slice(-1);
        $('#btnAddwork').click(function() {
                        var data = {work_id: id_of_work, number_of_work: ++w_num};
                        var html = _.template(worktemplate,data);
                        $('.values-jelement-work').append(html);
                        $('.input-append.date').datepicker();
                        });
        }
     if($('.values-jelement-education').length>0){ 
        var eductemplate = $("#getEducTemplate").html();
        var id_of_educ = $('.values-jelement-education').find('table').attr('id').slice(0,-2);
        var e_num = $('.values-jelement-education').find('table').attr('id').slice(-1);
        $('#btnAddeducation').click(function() {
                        var data = {educ_id: id_of_educ, number_of_edu: ++e_num};
                        var html = _.template(eductemplate,data);
                        $('.values-jelement-education').append(html);
                        $('.input-append.date').datepicker();
                        });
        }
    });
//turn this into backbone views
