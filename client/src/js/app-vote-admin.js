    $(function() {
    'use strict';

        function changeText(text, field) {
            $(field).fadeOut(200, function() {
                $(field).html(text).fadeIn(500);
            });
        }

        function setErrorMessage(type, message) {
            $('#messages').html('<div class="alert alert-' + type + '">' + message + '</div>').find('div').show().delay(2500).slideUp(500);
        }


        function ajaxFunction(self, event, success) {
            event.preventDefault();

            $.ajax({
                url: $(self).attr('href')
            }).done(function( data ) {
                if (data.success) {
                    success(data, self);

                    if (data.message) {
                        setErrorMessage('success', data.message);
                    }
                } else {
                    if (data.message) {
                        setErrorMessage('danger', data.message);
                    }
                }
            });
        }


        $('a.access').on('click', function(event) {
            ajaxFunction(this, event, function(data, self) {
                var accessCol = $(self).parent().parent().find('td:nth-child(2)');
                if (data.active) {
                    changeText('deaktivieren', self);
                    changeText('Benutzer', accessCol);
                } else {
                    changeText('aktivieren', self);
                    changeText('Inaktiv', accessCol);
                }
            });
        });

        $('a.mod').on('click', function(event) {
            ajaxFunction(this, event, function(data, self) {
                var accessCol = $(self).parent().parent().find('td:nth-child(2)');
                if (data.mod) {
                    changeText('degradieren', self);
                    changeText('Moderator', accessCol);
                } else {
                    changeText('befördern', self);
                    changeText('Benutzer', accessCol);
                }
            });
        });

        $('a.voteState').on('click', function(event) {
            ajaxFunction(this, event, function(data, self) {
                var stateCol = $(self).parent().parent().parent().parent().parent().find('td:nth-child(5)');
                if (data.state) {
                    changeText('Aus dem Voting nehmen', self);
                    changeText('Im Voting', stateCol);
                } else {
                    changeText('Ins Voting nehmen', self);
                    changeText('Aus Voting genommen', stateCol);
                }
            });
        });

        $('a.voteStateDetail').on('click', function(event) {
            ajaxFunction(this, event, function(data, self) {
                var stateCol = $('#voteState');
                console.log(stateCol);
                if (data.state) {
                    changeText('Aus dem Voting nehmen', self);
                    changeText('Im Voting', stateCol);
                } else {
                    changeText('Ins Voting nehmen', self);
                    changeText('Aus Voting genommen', stateCol);
                }
            });
        });

        $('a.distance').on('click', function(event) {
            ajaxFunction(this, event, function(data, self) {
                console.log(data);
                if (data.distance) {
                    changeText(data.distance + ' km', self);
                }
            });
        });


        /* Sort Users */
        var order = 2;

        /**
         * Generic handler for sorting a table by clicking on the column
         *
         * @param string table the id of the table
         * @param string elem the id of the elem the onclick-Listener should be registered on
         * @param int num the order-number (0,2,4, ...)
         * @param int col the nth-col (0,1,2,...)
         *
         * @return void
         * */
        function sortLinkHandler(table, elem, num, col) {
            $(elem).on('click', function (event) {
                event.preventDefault();
                order = (order < num) ? num : (num - 1);
                sortTable(col, order, table);
            });
        }

        /** Sort users */
        sortLinkHandler('#usersTable', '#sortLogin', 2, 0);
        sortLinkHandler('#usersTable', '#sortAccess', 4, 1);


        function sortBandTable(elem, num, col) {
            sortLinkHandler('#bandsTable', elem, num, col);
        }

        sortBandTable('#sortName', 2, 0);
        sortBandTable('#sortMembers', 4, 1);
        sortBandTable('#sortCity', 6, 2);
        sortBandTable('#sortDistance', 8, 3);
        sortBandTable('#sortState', 10, 4);
        sortBandTable('#sortCount', 12, 5);
        sortBandTable('#sortAverage', 14, 6);



        function sortTable(index, order, table) {
            var rows = $(table).find('tbody tr').get();

                rows.sort(function (a, b) {

                var A = $(a).children('td').eq(index).text().toLowerCase().trim();
                var B = $(b).children('td').eq(index).text().toLowerCase().trim();

                if (table === '#bandsTable') {
                    var matchesA, matchesB;

                    if (index === 1) {
                        A = (A === '?') ? 100 : parseInt(A);
                        B = (B === '?') ? 100 : parseInt(B);
                    } else if (index === 3) {
                        matchesA = A.match(/(\d{1,4}) km/);
                        matchesB = B.match(/(\d{1,4}) km/);
                        A = (matchesA) ? parseInt(matchesA[1]) : 20000;
                        B = (matchesB) ? parseInt(matchesB[1]) : 20000;
                    } else if (index === 5) {
                        A = parseInt(A);
                        B = parseInt(B);
                    } else if (index === 6) {
                        matchesA = A.match(/⌀ (\d\.\d)/);
                        matchesB = B.match(/⌀ (\d\.\d)/);
                        A = (matchesA) ? parseInt(matchesA[1]) : 0.0;
                        B = (matchesB) ? parseInt(matchesB[1]) : 0.0;
                    }
                }

                if (A < B) {
                    return (order % 2 === 1) ? 1 : -1;
                }

                if (A > B) {
                    return (order % 2 === 1) ? -1 : 1;
                }

                return 0;

            });

            $.each(rows, function (index, row) {
                $(table).children('tbody').append(row);
            });
        }
    });