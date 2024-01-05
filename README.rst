=====
gpush
=====

A small Python package for pushing files to Google Drive. To use it you need two things:

1. A Google Service Account (follow this `guide <https://cloud.google.com/iam/docs/creating-managing-service-accounts>`_ to create one)
2. A Google Drive folder where service account has editor permissions (detailed guide below)

gpush will search for the path to the service account file in the ``SERVICE_ACCOUNT_FILE`` environment variable and the folder location
in the ``FOLDER_ID`` environment variable. See the `Setting Up Google Drive Folder`_ section below for more details.

Setting Up Google Drive Folder
==============================

1. Go to Google Drive and create a new folder.
2. Name the folder appropriately for your project.
3. Right-click on the folder and select "Share."
4. Add the email address of the user you want to share the folder with, and set their permission level (e.g., Viewer, Commenter, Editor).
5. Once shared, right-click on the folder again and select "Get link."
6. Copy the folder ID from the link. The folder ID is the long string of letters and numbers in the URL.

Exporting Folder ID and Service Account File path as an Environment Variable
=====================================================================================

1. Open your terminal.
2. Use the export command to set the folder ID as an environment variable. Replace ``<FOLDER_ID>`` and ``<SERVICE_ACCOUNT_FILE_PATH>`` with your actual folder ID and path to ``SERVICE_ACCOUNT_FILE``::

    export FOLDER_ID=<FOLDER_ID>
    export SERVICE_ACCOUNT_FILE=<SERVICE_ACCOUNT_FILE_PATH>

3. To ensure the variables are set correctly, you can echo it::

    echo $FOLDER_ID
    echo $SERVICE_ACCOUNT_FILE

4. This environment variable can now be used in your application to reference the Google Drive folder.
5. To make the environment variable permanent, add the export command to your ``~/.profile`` file.

.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses ``pre-commit``, please make sure to install it before making any
changes::

    pip install pre-commit
    cd gpush
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
