/**
 * Django dynamic formsets v1.5.0
 *
 * @requires jQuery v1.2.6 or later
 *
 * @author Allan James Vestal (ajvestal@dallasnews.com)
 *
 * Originally developed by Stanislaus Madueke
 *
 * Copyright (c) 2016 Allan James Vestal, for
 * The Dallas Morning News (A.H. Belo Corporation).
 * All rights reserved.
 *
 * Released under the BSD License:
 * http://www.opensource.org/licenses/bsd-license.php
 */
;(function($) {
    $.fn.formset = function(opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts),
            flatExtraClasses = options.extraClasses.join(' '),
            totalForms = $('#id_' + options.prefix + '-TOTAL_FORMS'),
            maxForms = $('#id_' + options.prefix + '-MAX_NUM_FORMS'),
            minForms = $('#id_' + options.prefix + '-MIN_NUM_FORMS'),
            childElementSelector = 'input,select,textarea,label,div',
            $$ = $(this),
            allowInitialRender = (options.allowEmptyFormset) ? true : ($$.children().length),

            applyExtraClasses = function(row, ndx) {
                if (options.extraClasses) {
                    row.removeClass(flatExtraClasses);
                    row.addClass(options.extraClasses[ndx % options.extraClasses.length]);
                }
            },

            updateElementIndex = function(elem, prefix, ndx) {
                var idRegex = new RegExp(prefix + '-(\\d+|__prefix__)-'),
                    replacement = prefix + '-' + ndx + '-';
                if (elem.attr("for")) elem.attr("for", elem.attr("for").replace(idRegex, replacement));
                if (elem.attr('id')) elem.attr('id', elem.attr('id').replace(idRegex, replacement));
                if (elem.attr('name')) elem.attr('name', elem.attr('name').replace(idRegex, replacement));
            },

            hasChildElements = function(row) {
                return row.find(childElementSelector).length > 0;
            },

            showAddButton = function() {
                return maxForms.length == 0 ||   // For Django versions pre 1.2
                    (maxForms.val() == '' || (maxForms.val() - totalForms.val() > 0));
            },

            /**
            * Indicates whether delete link(s) can be displayed - when total forms > min forms
            */
            showDeleteLinks = function() {
                return minForms.length == 0 ||   // For Django versions pre 1.7
                    (minForms.val() == '' || (totalForms.val() - minForms.val() > 0));
            },

            insertDeleteLink = function(row) {
                var delCssSelector = $.trim(options.deleteCssClass).replace(/\s+/g, '.'),
                    addCssSelector = $.trim(options.addCssClass).replace(/\s+/g, '.'),
                    deleteTriggerMarkup = '<a ' +
                                            'class="' + options.deleteCssClass + '" ' +
                                            'href="javascript:void(0)">' +
                                                options.uiText.removePrompt +
                                            '</a>';

                if (row.is('TR')) {
                    // If the forms are laid out in table rows, insert
                    // the remove button into the last table cell:
                    row.children(':last').append(deleteTriggerMarkup);
                } else if (row.is('UL') || row.is('OL')) {
                    // If they're laid out as an ordered/unordered list,
                    // insert an <li> after the last list item:

                    row.append('<li>' + deleteTriggerMarkup + '</li>');
                } else {
                    // Otherwise, just insert the remove button as the
                    // last child element of the form's container:
                    row.append(deleteTriggerMarkup);
                }
                // Check if we're under the minimum number of forms - not to display delete link at rendering
                if (!showDeleteLinks()){
                    row.find('a.' + delCssSelector).hide();
                }

                row.find('a.' + delCssSelector).click(function() {
                    var row = $(this).parents('.' + options.formCssClass),
                        del = row.find('input:hidden[id $= "-DELETE"]'),
                        buttonRow = row.siblings("a." + addCssSelector + ', .' + options.formCssClass + '-add'),
                        forms;
                    if (del.length) {
                        // We're dealing with an inline formset.
                        // Rather than remove this form from the DOM, we'll mark it as deleted
                        // and hide it, then let Django handle the deleting:
                        del.val('on');
                        row.hide();
                        forms = $('.' + options.formCssClass).not(':hidden');
                    } else {
                        row.remove();
                        // Update the TOTAL_FORMS count:
                        forms = $('.' + options.formCssClass).not('.formset-custom-template');
                        totalForms.val(forms.length);
                    }
                    for (var i=0, formCount=forms.length; i<formCount; i++) {
                        // Apply `extraClasses` to form rows so they're nicely alternating:
                        applyExtraClasses(forms.eq(i), i);
                        if (!del.length) {
                            // Also update names and IDs for all child controls (if this isn't
                            // a delete-able inline formset) so they remain in sequence:
                            forms.eq(i).find(childElementSelector).each(function() {
                                updateElementIndex($(this), options.prefix, i);
                            });
                        }
                    }
                    // Check if we've reached the minimum number of forms - hide all delete link(s)
                    if (!showDeleteLinks()){
                        $('a.' + delCssSelector).each(function(){$(this).hide();});
                    }
                    // Check if we need to show the add button:
                    if (buttonRow.is(':hidden') && showAddButton()) buttonRow.show();
                    // If a post-delete callback was provided, call it with the deleted form:
                    if (options.callbacks.onRemove) options.callbacks.onRemove(row);
                    return false;
                });
            };

        function changeDeleteTrigger(row) {
            var del = row.find('input:checkbox[id $= "-DELETE"]');
            if (del.length) {
                // If you specify "can_delete = True" when creating an inline formset,
                // Django adds a checkbox to each form in the formset.
                // Replace the default checkbox with a hidden field:
                if (del.is(':checked')) {
                    // If an inline formset containing deleted forms fails validation, make sure
                    // we keep the forms hidden (thanks for the bug report and suggested fix Mike)
                    del.before('<input type="hidden" name="' + del.attr('name') +'" id="' + del.attr('id') +'" value="on" />');
                    row.hide();
                } else {
                    del.before('<input type="hidden" name="' + del.attr('name') +'" id="' + del.attr('id') +'" />');
                }
                // Hide any labels associated with the DELETE checkbox:
                $('label[for="' + del.attr('id') + '"]').hide();
                del.remove();
            }
        }

        $$.children().each(function(i) {
            var row = $(this);

            changeDeleteTrigger(row);

            if (hasChildElements(row)) {
                row.addClass(options.formCssClass);
                if (row.is(':visible')) {
                    insertDeleteLink(row);
                    applyExtraClasses(row, i);
                }
            }
        });

        if (allowInitialRender) {
            var hideAddButton = !showAddButton(),
                addButton, template;

            if (options.formTemplate) {
                // If a form template was specified, we'll clone it to generate new form instances:
                template = (options.formTemplate instanceof $) ? options.formTemplate : $(options.formTemplate);

                template.removeAttr('id').addClass(options.formCssClass + ' formset-custom-template');

                template.find(childElementSelector).each(function() {
                    var $elem = $(this);

                    updateElementIndex($elem, options.prefix, '__prefix__');

                    if ($elem.not.apply($elem, options.keepFieldValues).length > 0) {
                        // If this is a checkbox or radiobutton, uncheck it.
                        // This fixes Issue 1, reported by Wilson.Andrew.J:
                        if ($elem.is('input:checkbox') || $elem.is('input:radio')) {
                            $elem.attr('checked', false);
                        } else if ($elem.is('select')) {
                            $elem.find('option[selected="selected"]').removeAttr("selected");
                        } else {
                            $elem.val('');
                        }
                    }
                });
                insertDeleteLink(template);
            } else {
                // Otherwise, use the last form in the formset; this works much better if you've got
                // extra (>= 1) forms (thnaks to justhamade for pointing this out):
                template = $('.' + options.formCssClass + ':last').clone(true).removeAttr('id');
                template.find('input:hidden[id $= "-DELETE"]').remove();
                // Clear all cloned fields, except those the user wants to keep (thanks to brunogola for the suggestion):
                template.find(childElementSelector).not(options.keepFieldValues).each(function() {
                    var $elem = $(this);
                    // If this is a checkbox or radiobutton, uncheck it.
                    // This fixes Issue 1, reported by Wilson.Andrew.J:
                    if ($elem.is('input:checkbox') || $elem.is('input:radio')) {
                        $elem.attr('checked', false);
                    } else if ($elem.is('select')) {
                        $elem.find('option[selected="selected"]').removeAttr("selected");
                    } else {
                        $elem.val('');
                    }
                });
            }
            // FIXME: Perhaps using $.data would be a better idea?
            options.formTemplate = template;

            var addTriggerMarkup = '<a ' +
                                        'class="' + options.addCssClass + '" ' +
                                        'href="javascript:void(0)">' +
                                            options.uiText.addPrompt +
                                        '</a>';

            addButton = $(addTriggerMarkup);

            if (options.addButtonHolder) {
                // If a custom add-form button holder has been set, append the
                // add-form-button's HTML into that element.
                var addHolder = (options.addButtonHolder instanceof $) ? options.addButtonHolder : $(options.addButtonHolder);
                addHolder.append(addButton);
                if (hideAddButton) addButton.hide();
            } else {
                // Otherwise, insert it immediately after the formset:
                $$.after(addButton);
                if (hideAddButton) addButton.hide();
            }

            addButton.click(function() {
                var formCount = parseInt(totalForms.val()),
                    row = options.formTemplate.clone(true).removeClass('formset-custom-template'),
                    delCssSelector = $.trim(options.deleteCssClass).replace(/\s+/g, '.');

                applyExtraClasses(row, formCount);

                // Append the new form after all existing forms.
                // NOTE: We re-query elements based on the selector to be sure
                // we consider forms that have been added or removed in JS.
                $$.append(row);
                // $($$.selector).filter(':last').after(row);

                row.find(childElementSelector).each(function() {
                    updateElementIndex($(this), options.prefix, formCount);
                });

                changeDeleteTrigger(row);

                totalForms.val(formCount + 1);
                // Check if we're above the minimum allowed number of forms -> show all delete link(s)
                if (showDeleteLinks()){
                    $('a.' + delCssSelector).each(function(){$(this).show();});
                }
                // Check if we've exceeded the maximum allowed number of forms:
                if (!showAddButton()) {
                    addButton.hide();
                }

                // If a post-add callback was supplied, call it with the added form:
                if (options.callbacks.onAdd) options.callbacks.onAdd(row, formCount);
                return false;
            });

            if (options.callbacks.postInitialize) {
                options.callbacks.postInitialize($$);
            }
        }

        return $$;
    };

    /* Setup plugin defaults */
    $.fn.formset.defaults = {

        prefix: 'form',                  // The form prefix for your django formset
        allowEmptyFormset: false,        // Whether to initialize the formset JS when no initial forms are present.

        addButtonHolder: null,           // Where should the add button be placed?
        formTemplate: null,              // The jQuery selection cloned to generate new form instances

        addCssClass: 'add-row',          // CSS class applied to the add link
        deleteCssClass: 'delete-row',    // CSS class applied to the delete link
        formCssClass: 'dynamic-form',    // CSS class applied to each form in a formset
        extraClasses: [],                // Additional CSS classes, which will be applied to each form in turn


        callbacks: {
            onAdd: null,                 // Function called each time a new form is added.
            onRemove: null,              // Function called each time an existing form is deleted.
            postInitialize: null,        // Function called when the formset has been initialized.
        },
        keepFieldValues: '',             // jQuery selector for fields whose values should be kept when the form is cloned
        uiText: {
            addPrompt: 'Add another',         // Text used on the 'add a new form' control.
            removePrompt: 'Remove',        // Text used on the 'delete this existing form' control.
        },
    };
})(jQuery);