/* eslint-disable no-console,import/prefer-default-export */

/**
 * @description Console that prints messages in console while in debug-mode
 */

class Console {
  static debug() {
    return process.env.NODE_ENV !== 'production';
  }

  static combine(allMessages, message) {
    return `${allMessages} ${message}`;
  }

  /**
   * Function that logs messages in console
   * @param {Any} args - values that should be console.log'ged
   */
  static log(...args) {
    if (Console.debug) {
      console.log(args.reduce(Console.combine));
    }
  }

  /**
   * Function that prints error-messages in console
   * @param {String|Error} args - errores that should be console.error'ed
   */
  static error(...errors) {
    if (Console.debug) {
      console.error(errors.reduce(Console.combine));
    }
  }

  /**
   * Function that logs messages with info-symbol in console
   * @param {String|Error} args - Messages that should be console.info'ed
   */
  static info(...args) {
    if (Console.debug) {
      console.info(args.reduce(Console.combine));
    }
  }
}

// Named export to set a standard in the app.. might have to change late
export { Console };
