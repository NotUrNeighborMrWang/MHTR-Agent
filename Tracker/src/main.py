import os
import time
import sys
import datetime

import utils
import gptapi4vacuumDEMO as gptapi


def make_print_to_file(path='./log'):
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            self.path= os.path.join(path, filename)
            self.log = open(self.path, "a", encoding='utf8',)
            print("save:", os.path.join(self.path, filename))
 
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
 
        def flush(self):
            pass

 
    fileName = datetime.datetime.now().strftime('day'+'%Y_%m_%d')
    sys.stdout = Logger(fileName + '.log', path=path)

    print(fileName.center(60,'*'))


if __name__ == '__main__':
    
    make_print_to_file(path='./log')
    
    pdfs_df = utils.get_all_pdfs('../examples')  
     
    api_key = "your_API_key"

    
    for i_pdf, pdf_path in enumerate(pdfs_df['pdf_path']): 
        

        tic = time.time()
        print(f"\n============= Process #{i_pdf} =============")
        print('Start time:',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        pdf_name = pdf_path.split('/')[-1]
        print(f'Process #{i_pdf}:',pdf_path)

        print("------- Finf Table Page ... -------")
        tables_pages = utils.find_pages(pdf_path, r'\bTable\b')
        pdfs_df.loc[pdfs_df['pdf_path'] == pdf_path, 'tables_pages'] = str(tables_pages)
        print(f"Page number of tables: {tables_pages}")
        table_images = utils.get_pic_from_pdf(pdf_path,tables_pages)

        print("------- Finf References Page ... -------")
        references_pages = utils.find_pages(pdf_path, 'References|Notes and references|Acknowledgements|ACKNOWLEDGMENTS|REFERENCES|References and notes')
        print(f"Page number of references: {references_pages}")
        if len(references_pages) > 0:
            min_ref_page = min(references_pages)
        else:
            min_ref_page = utils.get_page_number(pdf_path)
        pdfs_df.loc[pdfs_df['pdf_path'] == pdf_path, 'min_ref_page'] = min_ref_page
    
        print("------- Extract Text ... -------")
        page1_text = utils.extract_text_from_page(pdf_path)
        all_pages_text = utils.extract_text_by_page_and_paragraph(pdf_path,min_ref_page)

        print('------- extracting table information use gpt4v ... -------')
        utils.extract_table_text(api_key,table_images)

        print('------- reading SI ... -------')
        SI_text = utils.read_SI(pdf_path)
        
        all_text = utils.gather_article_SI_table(pdf_path)
        print('------- all text gathered -------')
           
        print('------- extracting parameters table use gpt4 ... -------')
        base_dir = os.path.dirname(pdf_path)
        if not os.path.exists(f'{base_dir}/response/{pdf_name[:-4]}.json'):
            response_json = gptapi.use_gpt_4(api_key=api_key,input_information=all_text)
        
            if not os.path.exists(f'{base_dir}/response'):
                os.makedirs(f'{base_dir}/response')
            with open(f'{base_dir}/response/{pdf_name[:-4]}.json', 'w', encoding='utf-8') as f:
                f.write(response_json)
        else:
            print('response file already exists')
            response_json = open(f'{base_dir}/response/{pdf_name[:-4]}.json', 'r',encoding='utf-8').read()
        
        table_df = utils.process_response_md(response_json)
        table_df.to_excel(f'{base_dir}/response/{pdf_name[:-4]}.xlsx',index=False)

        toc = time.time()
        print('End Time:',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('Spend time(s):',toc-tic)

        if len(pdfs_df['pdf_path']) >= 2:
            time.sleep(30)
            
    print('*'*50)
    print('\n')