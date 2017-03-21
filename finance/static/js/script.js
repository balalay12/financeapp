$('#deleteAccount').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var data = button.data('account')
    acc = data.split(' ')
    var modal = $(this);
    modal.find('.modal-body p').text('Вы уверены что хотите удалить счет "' + acc[0] + '"')
    $('#deleteAccountForm').attr('action', '/account/delete/' + acc[1] + '/')
});

$('.datepicker').datepicker({
    format: "dd.mm.yyyy",
    language: "ru"
});
