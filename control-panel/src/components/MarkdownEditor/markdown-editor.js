/* eslint-disable */
import CodeMirror from 'codemirror';
window.CodeMirror = CodeMirror;

import showdown from 'showdown';
const converter = new showdown.Converter();

export default {
  name: 'MarkdownEditor',

  data() {
    return {
      // CodeMirror Options
      options: {
        mode: 'gfm',
      },

      tab: 'edit',

      html: '',
    };
  },

  methods: {
    switchTab(tab) {
      this.tab = tab;
      // show CodeMirror instance DOM
      const cmEle = this.editor.getWrapperElement();
      // cmEle.classList = cmEle.classList.replace('hide-cm-instance', '');
      cmEle.classList.remove('hide-cm-instance');

      if (tab === 'preview') {
        // hide CodeMirror intance DOM
        const cmEle = this.editor.getWrapperElement();
        cmEle.classList.add('hide-cm-instance');

        // convert markdown to html and show on page
        const content = this.editor.getValue();
        console.log('DEBUG got content', content);
        this.html = converter.makeHtml(content);
      }
    },
  },

  // boot-up
  mounted() {
    this.editor = new CodeMirror(this.$el, this.options);
  },
};
