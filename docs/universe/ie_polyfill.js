// from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign
if (typeof Object.assign != 'function') {
  // Must be writable: true, enumerable: false, configurable: true
  Object.defineProperty(Object, "assign", {
    value: function assign(target, varArgs) { // .length of function is 2
      'use strict';
      if (target == null) { // TypeError if undefined or null
        throw new TypeError('Cannot convert undefined or null to object');
      }

      var to = Object(target);

      for (var index = 1; index < arguments.length; index++) {
        var nextSource = arguments[index];

        if (nextSource != null) { // Skip over if undefined or null
          for (var nextKey in nextSource) {
            // Avoid bugs when hasOwnProperty is shadowed
            if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
              to[nextKey] = nextSource[nextKey];
            }
          }
        }
      }
      return to;
    },
    writable: true,
    configurable: true
  });
}



// From https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf
if (!Array.prototype.indexOf) {
  Array.prototype.indexOf = function indexOf(member, startFrom) {
      /*
      In non-strict mode, if the `this` variable is null or undefined, then it is
      set to the window object. Otherwise, `this` is automatically converted to an
      object. In strict mode, if the `this` variable is null or undefined, a
      `TypeError` is thrown.
      */
      if (this == null) {
          throw new TypeError("Array.prototype.indexOf() - can't convert `" + this + "` to object");
      }

      var
          index = isFinite(startFrom) ? Math.floor(startFrom) : 0,
          that = this instanceof Object ? this : new Object(this),
          length = isFinite(that.length) ? Math.floor(that.length) : 0;

      if (index >= length) {
          return -1;
      }

      if (index < 0) {
          index = Math.max(length + index, 0);
      }

      if (member === undefined) {
          /*
            Since `member` is undefined, keys that don't exist will have the same
            value as `member`, and thus do need to be checked.
          */
          do {
              if (index in that && that[index] === undefined) {
                  return index;
              }
          } while (++index < length);
      } else {
          do {
              if (that[index] === member) {
                  return index;
              }
          } while (++index < length);
      }

      return -1;
  };
}

// from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim
if (!String.prototype.trim) {
  String.prototype.trim = function () {
    return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '');
  };
}

// Console-polyfill. MIT license.
// https://github.com/paulmillr/console-polyfill
// Make it safe to do console.log() always.
(function(global) {
  'use strict';
  if (!global.console) {
    global.console = {};
  }
  var con = global.console;
  var prop, method;
  var dummy = function() {};
  var properties = ['memory'];
  var methods = ('assert,clear,count,debug,dir,dirxml,error,exception,group,' +
     'groupCollapsed,groupEnd,info,log,markTimeline,profile,profiles,profileEnd,' +
     'show,table,time,timeEnd,timeline,timelineEnd,timeStamp,trace,warn').split(',');
  while (prop = properties.pop()) if (!con[prop]) con[prop] = {};
  while (method = methods.pop()) if (!con[method]) con[method] = dummy;
  // Using `this` for web workers & supports Browserify / Webpack.
})(typeof window === 'undefined' ? this : window);