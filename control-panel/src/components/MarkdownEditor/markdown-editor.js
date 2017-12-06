/* eslint-disable */
import CodeMirror from 'codemirror';
window.CodeMirror = CodeMirror;
import * as _ from 'lodash';
import showdown from 'showdown';
const converter = new showdown.Converter();
import apis from '@/utils/api';
import toMarkdown from 'to-markdown';

export default {
  name: 'MarkdownEditor',

  data() {
    return {
      // CodeMirror Options
      options: {
        // 编辑器模式: Github Flavor Markdown
        mode: 'gfm',

        // 是否自动折行
        lineWrapping: true,

        // 是否显示行号
        lineNumbers: true,

        // 滚动条样式
        scrollbarStyle: 'native',

        // 自动获取焦点
        autofocus: true,
      },

      article: null,

      tab: 'edit',

      html: '',
    };
  },

  created() {
    if (this.$route.params.articleId) {
      apis.getArticle(this.$route.params.articleId)
        .then(res => {
          this.article = res;
          if (this.editor) {
            if (this.article.ext === 'html') {
              this.editor.setValue(toMarkdown(this.article.content));
            } else {
              this.editor.setValue(this.article.content);
            }

            this.editor.refresh();
          }
        });
    }
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
    if (this.article) {
      if (this.article.ext === 'html') {
        this.editor.setValue(toMarkdown(this.article.content));
      } else {
        this.editor.setValue(this.article.content);
      }

      this.editor.refresh();
    }
  },
};
