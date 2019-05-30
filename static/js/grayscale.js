(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 48)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 54
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 50) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  /*
   * Copyright (c) 2014 Mike King (@micjamking)
   *
   * jQuery Succinct plugin
   * Version 1.1.0 (October 2014)
   *
   * Licensed under the MIT License
   */
	
	$.fn.succinct = function(options) {

		var settings = $.extend({
				size: 240,
				omission: '...',
				ignore: true
			}, options);

		return this.each(function() {

			var textDefault,
				textTruncated,
				elements = $(this),
				regex    = /[!-\/:-@\[-`{-~]$/,
				init     = function() {
					elements.each(function() {
						textDefault = $(this).html();

						if (textDefault.length > settings.size) {
							textTruncated = $.trim(textDefault)
											.substring(0, settings.size)
											.split(' ')
											.slice(0, -1)
											.join(' ');

							if (settings.ignore) {
								textTruncated = textTruncated.replace(regex, '');
							}

							$(this).html(textTruncated + settings.omission);
						}
					});
				};
			init();
		});
	};
  
  
  $.fn.readMore = function(options) {

		// Options
		var defaults = {
			readMoreLinkClass: "read-more__link",
			readMoreText: "Read more",
			readLessText: "Read less",
			readMoreHeight: 150
		};

		// Merge deafults into options
		options = $.extend(defaults, options);

		var obj = $( this );

		/** Get the options of the selected element.
		*
		*  @param {object} refElement - An array of elements.
		*/
		function getRefElementOptions(refElement) {

			if ( typeof refElement.data( "options" ) !== "undefined" ) {
				this.collapsedHeight = refElement.data( "options" );
			} else {
				this.collapsedHeight = options.readMoreHeight;
			}

		}

		/** Create the read more link for each element selected.
		 *
		 *  @param {object} element - An array of elements.
		 */
		function addReadMoreElement(element) {

			element.each( function() {

				// Get the options for the specific element
				var $target = $( this );

				var refElementOptions = new getRefElementOptions( $target );

				// Create the read-more link
				$( this )
					.after( "<span>" + options.readMoreText + "</span>" )
					.next().addClass( options.readMoreLinkClass );
				// Set the initial state of the read more element to be collapsed
				$( this )
					.css({
					"height": refElementOptions.collapsedHeight,
					"overflow": "hidden"
					});
			});
		}

		addReadMoreElement(obj);

		// Action on clicking the read-more link
		$( "." + options.readMoreLinkClass ).click(function() {

			var $target = $( this ).prev();

			var refElementOptions = new getRefElementOptions( $target );

			// Expand or collapse the "more" text
			if ( $target.css( "overflow" ) === "hidden" ) {

				$target.css({
					"height": "auto",
					"overflow": "auto"
					});
				$target.addClass( "expanded" );
			} else {

				$target.css({
					"height": refElementOptions.collapsedHeight,
					"overflow": "hidden"
					});
				$target.removeClass( "expanded" );
			}

			// Change the "read more" word accordingly
			if ( $( this ).text() === options.readMoreText ) {
				$( this ).text( options.readLessText );
			} else {
				$( this ).text( options.readMoreText );
			}

		});
	};
  
})(jQuery); // End of use strict
