from flask import render_template, flash


def verify(form):
    if not form.validate_on_submit():
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')
        return False
    return True