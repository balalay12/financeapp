$('#deleteAccount').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var data = button.data('account')
    acc = data.split(' ')
    var modal = $(this);
    var id = acc.pop()
    modal.find('.modal-body p').text('Вы уверены что хотите удалить счет "' + acc.join(' ') + '"')
    $('#deleteAccountForm').attr('action', '/account/delete/' + id + '/')
});

$('.datepicker').datepicker({
    format: "dd.mm.yyyy",
    language: "ru"
});
