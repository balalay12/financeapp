$('#deleteAccount').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var data = button.data('account')
    acc = data.split(' ')
    var modal = $(this);
    modal.find('.modal-body p').text('Вы уверены что хотите удалить счет "' + acc[0] + '"')
    $('#deleteAccountForm').attr('action', '/account/delete/' + acc[1] + '/')
});

$('#selectOperation').on('change', function() {
  if (this.value == 'C') {
    var str = '<option disabled selected value> -- выберите категорию -- </option>' +
              '{% for category in inc_categories %}' +
              '<option value="{{ category.id }}">{{ category.name }}</option>' +
              '{% endfor %}'
    $('#selectCategory').html(str);
  } else {
    var str = '<option disabled selected value> -- выберите категорию -- </option>' +
              '<span>{% for category in cost_categories %}</span>' +
              '<option value="{{ category.id }}">{{ category.name }}</option>' +
              '{% endfor %}'
    $('#selectCategory').html(str);
  }
})
